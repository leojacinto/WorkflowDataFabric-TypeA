#!/usr/bin/env python3
"""
Demo Hub WDF Lab Instance Prep — Web UI
Imports update sets and XML unloads into a ServiceNow Demo Hub instance.

Usage:
    python demo_hub_prep.py

Opens a browser at http://localhost:5000 with a form to enter instance details.
Credentials are used in-memory only and never stored to disk.
"""

import os
import re
import sys
import time
import json
import glob
import threading
import webbrowser
import xml.etree.ElementTree as ET
from queue import Queue

import requests
import urllib3
from flask import Flask, render_template_string, request, Response, jsonify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------------------------
# Resolve paths relative to this script (works inside zip or cloned repo)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# update_sets/ and xml_unloads/ sit one level up from app/
PARENT_DIR = os.path.dirname(BASE_DIR)
UPDATE_SET_DIR = os.path.join(PARENT_DIR, "update_sets")
XML_UNLOAD_DIR = os.path.join(PARENT_DIR, "xml_unloads")

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Store running jobs: job_id -> { status, log_queue, ... }
jobs = {}
job_lock = threading.Lock()


# ===========================================================================
# ServiceNow Client
# ===========================================================================
class SNClient:
    """Manages cookie-based UI session and REST API session."""

    def __init__(self, instance_url, username, password, log_fn=None):
        self.instance = instance_url.rstrip("/")
        self.username = username
        self.password = password
        self.log = log_fn or print

        self.ui = requests.Session()
        self.api = requests.Session()
        self.api.auth = (self.username, self.password)
        self.api.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.ck = None

    def login(self):
        self.log("Logging in...")
        for attempt in range(3):
            try:
                self.ui.post(f'{self.instance}/login.do', data={
                    'user_name': self.username,
                    'user_password': self.password,
                    'sys_action': 'sysverb_login'
                }, allow_redirects=True, timeout=120)
                break
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                self.log(f"  Login error (attempt {attempt+1}/3): {type(e).__name__}, retrying...")
                time.sleep(10)
        self._refresh_ck()
        if self.ck:
            self.log(f"  Logged in successfully.")
        else:
            self.log("  WARNING: Could not obtain CK token.")

    def _refresh_ck(self):
        for attempt in range(3):
            try:
                resp = self.ui.get(f'{self.instance}/sys.scripts.do', timeout=60)
                m = re.search(r"g_ck\s*=\s*'([^']+)'", resp.text)
                if not m:
                    m = re.search(r"var CK = '([^']+)'", resp.text)
                if not m:
                    m = re.search(r'name="sysparm_ck"[^>]*value="([^"]+)"', resp.text)
                self.ck = m.group(1) if m else ''
                if self.ck:
                    return
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                self.log(f"  CK refresh error (attempt {attempt+1}/3): {type(e).__name__}")
                time.sleep(5)

    def api_get(self, table, sys_id=None, params=None):
        url = f'{self.instance}/api/now/table/{table}'
        if sys_id:
            url += f'/{sys_id}'
        r = self.api.get(url, params=params)
        if r.status_code == 200:
            return r.json().get('result')
        return None

    def api_patch(self, table, sys_id, data):
        r = self.api.patch(
            f'{self.instance}/api/now/table/{table}/{sys_id}',
            json=data)
        if r.status_code in [200, 204]:
            return r.json().get('result') if r.status_code == 200 else True
        return None

    def upload_file(self, filepath, target_table):
        fname = os.path.basename(filepath)
        for attempt in range(3):
            try:
                self.log(f"  Uploading {fname}...")
                with open(filepath, 'rb') as f:
                    resp = self.ui.post(f'{self.instance}/sys_upload.do',
                        data={
                            'sysparm_ck': self.ck,
                            'sysparm_referring_url': f'{target_table}_list.do',
                            'sysparm_target': target_table,
                        },
                        files={'attachFile': (fname, f, 'application/xml')},
                        allow_redirects=False,
                        timeout=300
                    )
                success = resp.status_code in [200, 301, 302, 303]
                if success:
                    self.log(f"  Upload OK")
                    return True
                self.log(f"  Upload failed (HTTP {resp.status_code})")
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                self.log(f"  Upload error (attempt {attempt+1}/3): {type(e).__name__}")
                time.sleep(10)
                self.login()
        return False

    def run_bg_script(self, script):
        for attempt in range(3):
            try:
                resp = self.ui.post(f'{self.instance}/sys.scripts.do', data={
                    'sysparm_ck': self.ck,
                    'script': script,
                    'runscript': 'Run script',
                    'quota_managed_transaction': 'on',
                }, timeout=180)
                body = re.sub(r'<[^>]+>', ' ', resp.text)
                body = re.sub(r'\s+', ' ', body).strip()
                idx = body.find('Script:')
                output = body[idx:idx+400].strip() if idx >= 0 else ''
                return resp.status_code == 200, output
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                self.log(f"  BG script error (attempt {attempt+1}/3): {type(e).__name__}")
                time.sleep(10)
                self.login()
        return False, 'All retries failed'


# ===========================================================================
# Update Set Logic
# ===========================================================================
def analyze_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    records = root.findall('sys_remote_update_set')
    update_xmls = root.findall('sys_update_xml')
    if not records:
        return None
    seen = set()
    unique_records = []
    for r in records:
        sid = r.find('sys_id')
        if sid is not None and sid.text not in seen:
            seen.add(sid.text)
            unique_records.append(r)
    first = unique_records[0]
    sid = first.find('sys_id').text if first.find('sys_id') is not None else None
    name = first.find('name').text if first.find('name') is not None else None
    is_batch = len(unique_records) > 1
    return {
        'sys_id': sid, 'name': name, 'is_batch': is_batch,
        'record_count': len(unique_records), 'xml_count': len(update_xmls),
    }


def find_update_set_by_name(client, name):
    results = client.api_get('sys_remote_update_set', params={
        'sysparm_query': f'name={name}^ORDERBYDESCsys_created_on',
        'sysparm_fields': 'sys_id,name,state',
        'sysparm_limit': '1'
    })
    if results and isinstance(results, list) and len(results) > 0:
        return results[0]
    return None


def wait_for_state(client, sys_id, target_states, timeout=600, label="operation"):
    start = time.time()
    last_log = 0
    while time.time() - start < timeout:
        time.sleep(5)
        info = client.api_get('sys_remote_update_set', sys_id,
                              params={'sysparm_fields': 'state,name'})
        if info and isinstance(info, dict):
            state = info.get('state', '')
            elapsed = int(time.time() - start)
            if state in target_states:
                client.log(f"  {label} done. state={state} ({elapsed}s)")
                return state
            if elapsed - last_log >= 30:
                client.log(f"    Waiting... state={state} ({elapsed}s)")
                last_log = elapsed
    client.log(f"  {label} timed out after {timeout}s")
    return None


def preview(client, sys_id, is_batch):
    if is_batch:
        method = 'generateForHierarchy'
        label = 'Batch'
    else:
        method = 'generatePreviewRecordsWithUpdate'
        label = 'Single'
    script = f"""
var gr = new GlideRecord('sys_remote_update_set');
if (gr.get('{sys_id}')) {{
    gr.state = 'previewing';
    gr.update();
    var worker = new GlideScriptedHierarchicalWorker();
    worker.setProgressName('{label} Preview for: ' + gr.name);
    worker.setScriptIncludeName('UpdateSetPreviewer');
    worker.setScriptIncludeMethod('{method}');
    worker.putMethodArg('sys_id', gr.sys_id.toString());
    worker.setSource(gr.sys_id.toString());
    worker.setSourceTable('sys_remote_update_set');
    worker.setBackground(true);
    worker.setCannotCancel(true);
    worker.start();
    gs.print('Preview started: ' + worker.getProgressID());
}} else {{
    gs.print('ERROR: not found');
}}
"""
    ok, output = client.run_bg_script(script)
    client.log(f"  {output}")
    return ok


def commit(client, sys_id, is_batch):
    if is_batch:
        script = f"""
var gr = new GlideRecord('sys_remote_update_set');
if (gr.get('{sys_id}')) {{
    var starter = new SNC.HierarchyUpdateSetScriptable();
    var trackerId = starter.commitHierarchy(gr.sys_id.toString());
    gs.print('Hierarchy commit started. Tracker: ' + trackerId);
}} else {{
    gs.print('ERROR: not found');
}}
"""
    else:
        script = f"""
var rus = new GlideRecord('sys_remote_update_set');
rus.addQuery('sys_id', '{sys_id}');
rus.query();
if (rus.next()) {{
    var worker = new GlideUpdateSetWorker();
    var lus = new GlideRecord('sys_update_set');
    var lus_sysid = worker.remoteUpdateSetCommit(lus, rus, rus.update_source.url + '');
    var xml = new GlideRecord('sys_update_xml');
    xml.addQuery('remote_update_set', rus.sys_id);
    xml.query();
    while (xml.next()) {{
        xml.update_set = lus_sysid;
        xml.update();
    }}
    rus.update();
    worker.setUpdateSetSysId(lus_sysid);
    worker.setProgressName('Committing: ' + rus.name);
    worker.setBackground(true);
    worker.start();
    gs.print('Commit started: ' + lus_sysid);
}} else {{
    gs.print('ERROR: not found');
}}
"""
    ok, output = client.run_bg_script(script)
    client.log(f"  {output}")
    return ok


def accept_all_preview_errors(client, sys_id, is_batch=False):
    ids_to_check = [sys_id]
    if is_batch:
        children = client.api_get('sys_remote_update_set', params={
            'sysparm_query': f'remote_base_update_set={sys_id}',
            'sysparm_fields': 'sys_id',
            'sysparm_limit': '50'
        })
        if children:
            for c in children:
                ids_to_check.append(c['sys_id'])
    total_accepted, total_failed = 0, 0
    for check_id in ids_to_check:
        problems = client.api_get('sys_update_preview_problem', params={
            'sysparm_query': f'remote_update_set={check_id}',
            'sysparm_fields': 'sys_id',
            'sysparm_limit': '500'
        })
        if problems:
            for p in problems:
                result = client.api_patch('sys_update_preview_problem', p['sys_id'],
                                          {'disposition': 'accept'})
                if result:
                    total_accepted += 1
                else:
                    total_failed += 1
    if total_accepted or total_failed:
        client.log(f"  Accepted {total_accepted} preview problems (failed={total_failed})")
    else:
        client.log("  No preview problems.")


def process_update_set(client, xml_file):
    fname = os.path.basename(xml_file)
    client.log(f"\n--- Update Set: {fname} ---")

    meta = analyze_xml(xml_file)
    if not meta:
        client.log("  ERROR: No sys_remote_update_set element found")
        return 'PARSE_ERROR'

    sys_id = meta['sys_id']
    is_batch = meta['is_batch']
    client.log(f"  Name: {meta['name']}")
    client.log(f"  Type: {'BATCH' if is_batch else 'SINGLE'} ({meta['record_count']} sets, {meta['xml_count']} xml)")

    # Check if already committed
    if sys_id:
        info = client.api_get('sys_remote_update_set', sys_id,
                              params={'sysparm_fields': 'state,name'})
        if info and isinstance(info, dict):
            state = info.get('state', '')
            if state == 'committed':
                client.log(f"  Already committed — skipping.")
                return 'ALREADY_COMMITTED'

    # Upload
    if not client.upload_file(xml_file, 'sys_remote_update_set'):
        return 'UPLOAD_FAILED'
    time.sleep(3)

    # Verify
    if meta['name']:
        found = find_update_set_by_name(client, meta['name'])
        if found:
            sys_id = found['sys_id']
    if not sys_id:
        client.log("  ERROR: Could not find uploaded update set")
        return 'UPLOAD_FAILED'

    # Preview
    client.log("  Previewing...")
    if not preview(client, sys_id, is_batch):
        return 'PREVIEW_FAILED'
    state = wait_for_state(client, sys_id, ['previewed', 'committed'], timeout=600, label="Preview")
    if state == 'committed':
        return 'ALREADY_COMMITTED'
    if state != 'previewed':
        return 'PREVIEW_FAILED'

    # Accept errors
    accept_all_preview_errors(client, sys_id, is_batch=is_batch)

    # Commit
    client.log("  Committing...")
    if not commit(client, sys_id, is_batch):
        return 'COMMIT_FAILED'
    state = wait_for_state(client, sys_id, ['committed'], timeout=600, label="Commit")
    if state == 'committed':
        return 'SUCCESS'
    return 'COMMIT_FAILED'


def process_xml_unload(client, xml_file, target_table):
    fname = os.path.basename(xml_file)
    client.log(f"\n--- XML Unload: {fname} -> {target_table} ---")
    if not client.upload_file(xml_file, target_table):
        return 'UPLOAD_FAILED'
    return 'SUCCESS'


# ===========================================================================
# Discover XML files and unload mapping
# ===========================================================================
def discover_update_sets():
    """Return sorted list of XML files in update_sets/ directory."""
    if not os.path.isdir(UPDATE_SET_DIR):
        return []
    files = sorted(glob.glob(os.path.join(UPDATE_SET_DIR, "*.xml")))
    return files


def discover_xml_unloads():
    """Return list of {file, table} dicts from xml_unloads/ directory.

    Convention: filename should start with NN_ followed by the table name,
    e.g. '01_sn_erp_integration_cost_center.xml'
    The table name is extracted from the filename (everything between first _ and .xml).
    """
    if not os.path.isdir(XML_UNLOAD_DIR):
        return []
    files = sorted(glob.glob(os.path.join(XML_UNLOAD_DIR, "*.xml")))
    tasks = []
    for f in files:
        basename = os.path.splitext(os.path.basename(f))[0]
        # Strip leading number prefix: "01_table_name" -> "table_name"
        parts = basename.split('_', 1)
        if len(parts) == 2 and parts[0].isdigit():
            table = parts[1]
        else:
            table = basename
        tasks.append({'file': f, 'table': table})
    return tasks


# ===========================================================================
# Job runner (background thread)
# ===========================================================================
def run_import_job(job_id, instance_name, username, password):
    """Run the full import pipeline in a background thread."""
    q = jobs[job_id]['queue']

    def log(msg):
        q.put(msg)

    instance_url = f"https://{instance_name}.service-now.com"
    log(f"Target: {instance_url}")
    log(f"User: {username}")
    log("Password will NOT be stored. It is used in-memory only for this session.\n")

    # Test connection
    try:
        client = SNClient(instance_url, username, password, log_fn=log)
        client.login()
    except Exception as e:
        log(f"\nERROR: Failed to connect to {instance_url}")
        log(f"  {type(e).__name__}: {e}")
        log("\nPlease check your instance name and credentials.")
        jobs[job_id]['status'] = 'failed'
        q.put(None)  # sentinel
        return

    # Phase 1: Update Sets
    update_set_files = discover_update_sets()
    xml_unload_tasks = discover_xml_unloads()

    total = len(update_set_files) + len(xml_unload_tasks)
    log(f"\nFound {len(update_set_files)} update sets and {len(xml_unload_tasks)} XML unloads.")
    log(f"Total operations: {total}\n")

    results = {}
    step = 0

    if update_set_files:
        log("=" * 50)
        log("PHASE 1: Update Sets")
        log("=" * 50)
        for xml_file in update_set_files:
            step += 1
            fname = os.path.basename(xml_file)
            log(f"\n[{step}/{total}] {fname}")
            try:
                status = process_update_set(client, xml_file)
            except Exception as e:
                log(f"  EXCEPTION: {type(e).__name__}: {e}")
                status = 'ERROR'
            results[fname] = status
            ok = "OK" if status in ('SUCCESS', 'ALREADY_COMMITTED') else "FAIL"
            log(f"  Result: [{ok}] {status}")

    if xml_unload_tasks:
        log("\n" + "=" * 50)
        log("PHASE 2: XML Unloads")
        log("=" * 50)
        for task in xml_unload_tasks:
            step += 1
            fname = os.path.basename(task['file'])
            log(f"\n[{step}/{total}] {fname} -> {task['table']}")
            try:
                status = process_xml_unload(client, task['file'], task['table'])
            except Exception as e:
                log(f"  EXCEPTION: {type(e).__name__}: {e}")
                status = 'ERROR'
            results[fname] = status
            ok = "OK" if status == 'SUCCESS' else "FAIL"
            log(f"  Result: [{ok}] {status}")

    # Summary
    log("\n" + "=" * 50)
    log("SUMMARY")
    log("=" * 50)
    success_count = sum(1 for s in results.values() if s in ('SUCCESS', 'ALREADY_COMMITTED'))
    fail_count = len(results) - success_count
    for fn, st in results.items():
        sym = "OK" if st in ('SUCCESS', 'ALREADY_COMMITTED') else "FAIL"
        log(f"  [{sym}] {st:25s} {fn}")
    log(f"\nDone: {success_count} succeeded, {fail_count} failed out of {len(results)} total.")

    jobs[job_id]['status'] = 'completed' if fail_count == 0 else 'completed_with_errors'
    q.put(None)  # sentinel


def run_multi_import_job(job_id, instances):
    """Run imports for multiple instances sequentially (multi-tab admin mode)."""
    q = jobs[job_id]['queue']

    def log(msg):
        q.put(msg)

    log(f"Multi-instance mode: {len(instances)} instances queued.\n")

    overall_results = {}

    for idx, inst in enumerate(instances):
        instance_name = inst['instance']
        username = inst['username']
        password = inst['password']

        log("\n" + "#" * 60)
        log(f"# INSTANCE {idx+1}/{len(instances)}: {instance_name}")
        log("#" * 60)

        instance_url = f"https://{instance_name}.service-now.com"
        log(f"Target: {instance_url}")
        log(f"User: {username}\n")

        try:
            client = SNClient(instance_url, username, password, log_fn=log)
            client.login()
        except Exception as e:
            log(f"\nERROR: Failed to connect to {instance_url}")
            log(f"  {type(e).__name__}: {e}")
            overall_results[instance_name] = 'CONNECTION_FAILED'
            continue

        update_set_files = discover_update_sets()
        xml_unload_tasks = discover_xml_unloads()
        total = len(update_set_files) + len(xml_unload_tasks)
        instance_ok = True
        step = 0

        for xml_file in update_set_files:
            step += 1
            fname = os.path.basename(xml_file)
            log(f"\n[{step}/{total}] {fname}")
            try:
                status = process_update_set(client, xml_file)
            except Exception as e:
                log(f"  EXCEPTION: {type(e).__name__}: {e}")
                status = 'ERROR'
            ok = "OK" if status in ('SUCCESS', 'ALREADY_COMMITTED') else "FAIL"
            log(f"  Result: [{ok}] {status}")
            if ok == "FAIL":
                instance_ok = False

        for task in xml_unload_tasks:
            step += 1
            fname = os.path.basename(task['file'])
            log(f"\n[{step}/{total}] {fname} -> {task['table']}")
            try:
                status = process_xml_unload(client, task['file'], task['table'])
            except Exception as e:
                log(f"  EXCEPTION: {type(e).__name__}: {e}")
                status = 'ERROR'
            ok = "OK" if status == 'SUCCESS' else "FAIL"
            log(f"  Result: [{ok}] {status}")
            if ok == "FAIL":
                instance_ok = False

        overall_results[instance_name] = 'OK' if instance_ok else 'ERRORS'

    log("\n" + "#" * 60)
    log("# OVERALL SUMMARY")
    log("#" * 60)
    for inst, result in overall_results.items():
        log(f"  {inst}: {result}")

    jobs[job_id]['status'] = 'completed'
    q.put(None)


# ===========================================================================
# HTML Template (embedded — no external files needed)
# ===========================================================================
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Demo Hub WDF Lab — Instance Prep</title>
<style>
  :root {
    --bg: #0f172a; --surface: #1e293b; --surface2: #334155;
    --text: #e2e8f0; --text-muted: #94a3b8; --accent: #38bdf8;
    --green: #4ade80; --red: #f87171; --orange: #fb923c;
    --border: #475569; --radius: 8px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg); color: var(--text); min-height: 100vh;
    display: flex; flex-direction: column; align-items: center;
    padding: 2rem 1rem;
  }
  h1 { color: var(--accent); margin-bottom: 0.25rem; font-size: 1.5rem; }
  .subtitle { color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem; }
  .security-note {
    background: #1a2332; border: 1px solid #2d4a5e; border-radius: var(--radius);
    padding: 0.75rem 1rem; margin-bottom: 1.5rem; max-width: 700px; width: 100%;
    font-size: 0.85rem; color: var(--green);
  }
  .security-note strong { color: var(--green); }
  .container { max-width: 700px; width: 100%; }
  .tabs {
    display: flex; gap: 0; margin-bottom: 0; border-bottom: 2px solid var(--surface2);
  }
  .tab {
    padding: 0.75rem 1.5rem; cursor: pointer; background: transparent;
    border: none; color: var(--text-muted); font-size: 0.95rem;
    border-bottom: 2px solid transparent; margin-bottom: -2px;
    transition: all 0.2s;
  }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--accent); border-bottom-color: var(--accent); }
  .panel { display: none; background: var(--surface); border-radius: 0 0 var(--radius) var(--radius); padding: 1.5rem; }
  .panel.active { display: block; }
  label { display: block; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.25rem; margin-top: 0.75rem; }
  input, textarea {
    width: 100%; padding: 0.6rem 0.75rem; background: var(--bg); border: 1px solid var(--border);
    border-radius: var(--radius); color: var(--text); font-size: 0.95rem; outline: none;
  }
  input:focus, textarea:focus { border-color: var(--accent); }
  .input-hint { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem; }
  .btn {
    margin-top: 1.25rem; padding: 0.7rem 2rem; border: none; border-radius: var(--radius);
    font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
    background: var(--accent); color: var(--bg); width: 100%;
  }
  .btn:hover { filter: brightness(1.1); }
  .btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .log-container {
    margin-top: 1.5rem; background: #0c1222; border: 1px solid var(--border);
    border-radius: var(--radius); padding: 1rem; max-height: 500px; overflow-y: auto;
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 0.8rem;
    line-height: 1.5; white-space: pre-wrap; word-break: break-word; display: none;
  }
  .log-container.visible { display: block; }
  .status-bar {
    margin-top: 1rem; padding: 0.5rem 1rem; border-radius: var(--radius);
    font-weight: 600; text-align: center; display: none;
  }
  .status-bar.visible { display: block; }
  .status-bar.running { background: #1e3a5f; color: var(--accent); }
  .status-bar.success { background: #14532d; color: var(--green); }
  .status-bar.error { background: #451a1a; color: var(--red); }
  .multi-row { display: flex; gap: 0.5rem; align-items: end; margin-bottom: 0.5rem; }
  .multi-row input { flex: 1; }
  .multi-row .remove-btn {
    padding: 0.6rem 0.75rem; background: var(--red); color: white;
    border: none; border-radius: var(--radius); cursor: pointer; font-size: 0.85rem;
    white-space: nowrap;
  }
  .add-btn {
    margin-top: 0.5rem; padding: 0.5rem 1rem; background: var(--surface2);
    border: 1px solid var(--border); border-radius: var(--radius);
    color: var(--text); cursor: pointer; font-size: 0.85rem;
  }
  .add-btn:hover { background: var(--border); }
  .file-list {
    margin-top: 1rem; background: var(--bg); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 0.75rem; font-size: 0.8rem;
    max-height: 200px; overflow-y: auto;
  }
  .file-list div { padding: 0.15rem 0; color: var(--text-muted); }
  .file-list .section-label { color: var(--accent); font-weight: 600; margin-top: 0.5rem; }
</style>
</head>
<body>
<h1>Demo Hub WDF Lab — Instance Prep</h1>
<p class="subtitle">Import update sets and data into your ServiceNow Demo Hub instance</p>
<div class="security-note">
  <strong>🔒 Your credentials are safe.</strong> Your password is used in-memory only to connect
  to your ServiceNow instance. It is <strong>never stored</strong> to disk, logged, or transmitted
  anywhere other than directly to your instance.
</div>
<div class="container">
  <div class="tabs">
    <button class="tab active" onclick="switchTab('single')">Single Instance</button>
    <button class="tab" onclick="switchTab('multi')">Multi Instance (Admin)</button>
  </div>

  <!-- Single Instance Panel -->
  <div id="panel-single" class="panel active">
    <label for="instance">Instance Name</label>
    <input type="text" id="instance" placeholder="e.g. mycompany" autocomplete="off">
    <div class="input-hint">We'll connect to https://&lt;name&gt;.service-now.com</div>

    <label for="username">Username</label>
    <input type="text" id="username" placeholder="e.g. admin" autocomplete="off">

    <label for="password">Password</label>
    <input type="password" id="password" placeholder="Enter password" autocomplete="off">

    <div id="file-list-single" class="file-list"></div>

    <button class="btn" id="btn-single" onclick="startSingle()">Start Instance Prep</button>

    <div id="status-single" class="status-bar"></div>
    <div id="log-single" class="log-container"></div>
  </div>

  <!-- Multi Instance Panel -->
  <div id="panel-multi" class="panel">
    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
      Run the same import across multiple instances. Enter each instance's details below.
    </p>
    <div id="multi-instances">
      <div class="multi-row" data-idx="0">
        <input type="text" placeholder="Instance name" class="m-instance">
        <input type="text" placeholder="Username" class="m-username">
        <input type="password" placeholder="Password" class="m-password">
        <button class="remove-btn" onclick="removeRow(this)">✕</button>
      </div>
    </div>
    <button class="add-btn" onclick="addRow()">+ Add Instance</button>

    <button class="btn" id="btn-multi" onclick="startMulti()">Start All Instances</button>

    <div id="status-multi" class="status-bar"></div>
    <div id="log-multi" class="log-container"></div>
  </div>
</div>

<script>
function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + tab).classList.add('active');
  event.target.classList.add('active');
}

function addRow() {
  const container = document.getElementById('multi-instances');
  const div = document.createElement('div');
  div.className = 'multi-row';
  div.innerHTML = `
    <input type="text" placeholder="Instance name" class="m-instance">
    <input type="text" placeholder="Username" class="m-username">
    <input type="password" placeholder="Password" class="m-password">
    <button class="remove-btn" onclick="removeRow(this)">✕</button>
  `;
  container.appendChild(div);
}

function removeRow(btn) {
  const container = document.getElementById('multi-instances');
  if (container.children.length > 1) {
    btn.parentElement.remove();
  }
}

// Load file list on page load
fetch('/api/files').then(r => r.json()).then(data => {
  const el = document.getElementById('file-list-single');
  let html = '';
  if (data.update_sets.length) {
    html += '<div class="section-label">Update Sets (' + data.update_sets.length + ')</div>';
    data.update_sets.forEach(f => { html += '<div>' + f + '</div>'; });
  }
  if (data.xml_unloads.length) {
    html += '<div class="section-label" style="margin-top:0.5rem">XML Unloads (' + data.xml_unloads.length + ')</div>';
    data.xml_unloads.forEach(f => { html += '<div>' + f.file + ' → ' + f.table + '</div>'; });
  }
  if (!data.update_sets.length && !data.xml_unloads.length) {
    html = '<div style="color:var(--red)">No XML files found in update_sets/ or xml_unloads/ directories.</div>';
  }
  el.innerHTML = html;
});

function startSingle() {
  const instance = document.getElementById('instance').value.trim();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  if (!instance || !username || !password) {
    alert('Please fill in all fields.'); return;
  }
  const btn = document.getElementById('btn-single');
  btn.disabled = true; btn.textContent = 'Running...';
  const logEl = document.getElementById('log-single');
  const statusEl = document.getElementById('status-single');
  logEl.classList.add('visible'); logEl.textContent = '';
  statusEl.className = 'status-bar visible running';
  statusEl.textContent = 'Running — please wait...';

  fetch('/api/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({mode: 'single', instance, username, password})
  }).then(r => r.json()).then(data => {
    streamLog(data.job_id, logEl, statusEl, btn, 'Start Instance Prep');
  });
}

function startMulti() {
  const rows = document.querySelectorAll('#multi-instances .multi-row');
  const instances = [];
  rows.forEach(row => {
    const inst = row.querySelector('.m-instance').value.trim();
    const user = row.querySelector('.m-username').value.trim();
    const pass = row.querySelector('.m-password').value;
    if (inst && user && pass) instances.push({instance: inst, username: user, password: pass});
  });
  if (instances.length === 0) {
    alert('Please fill in at least one complete row.'); return;
  }
  const btn = document.getElementById('btn-multi');
  btn.disabled = true; btn.textContent = 'Running...';
  const logEl = document.getElementById('log-multi');
  const statusEl = document.getElementById('status-multi');
  logEl.classList.add('visible'); logEl.textContent = '';
  statusEl.className = 'status-bar visible running';
  statusEl.textContent = 'Running — please wait...';

  fetch('/api/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({mode: 'multi', instances})
  }).then(r => r.json()).then(data => {
    streamLog(data.job_id, logEl, statusEl, btn, 'Start All Instances');
  });
}

function streamLog(jobId, logEl, statusEl, btn, btnLabel) {
  const evtSource = new EventSource('/api/stream/' + jobId);
  evtSource.onmessage = function(e) {
    if (e.data === '__DONE__') {
      evtSource.close();
      btn.disabled = false; btn.textContent = btnLabel;
      statusEl.className = 'status-bar visible success';
      statusEl.textContent = 'Completed!';
      return;
    }
    if (e.data === '__DONE_WITH_ERRORS__') {
      evtSource.close();
      btn.disabled = false; btn.textContent = btnLabel;
      statusEl.className = 'status-bar visible error';
      statusEl.textContent = 'Completed with errors — check log above.';
      return;
    }
    logEl.textContent += e.data + '\n';
    logEl.scrollTop = logEl.scrollHeight;
  };
  evtSource.onerror = function() {
    evtSource.close();
    btn.disabled = false; btn.textContent = btnLabel;
  };
}
</script>
</body>
</html>
"""


# ===========================================================================
# Flask Routes
# ===========================================================================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/files')
def api_files():
    update_sets = [os.path.basename(f) for f in discover_update_sets()]
    xml_unloads = []
    for task in discover_xml_unloads():
        xml_unloads.append({
            'file': os.path.basename(task['file']),
            'table': task['table']
        })
    return jsonify({'update_sets': update_sets, 'xml_unloads': xml_unloads})


@app.route('/api/start', methods=['POST'])
def api_start():
    data = request.get_json()
    job_id = f"job_{int(time.time())}_{threading.current_thread().ident}"

    with job_lock:
        jobs[job_id] = {
            'status': 'running',
            'queue': Queue(),
        }

    if data.get('mode') == 'multi':
        instances = data.get('instances', [])
        t = threading.Thread(target=run_multi_import_job, args=(job_id, instances), daemon=True)
    else:
        instance_name = data['instance']
        username = data['username']
        password = data['password']
        t = threading.Thread(target=run_import_job,
                             args=(job_id, instance_name, username, password), daemon=True)
    t.start()
    return jsonify({'job_id': job_id})


@app.route('/api/stream/<job_id>')
def api_stream(job_id):
    def generate():
        if job_id not in jobs:
            yield "data: ERROR: Job not found\n\n"
            return
        q = jobs[job_id]['queue']
        while True:
            msg = q.get()
            if msg is None:
                status = jobs[job_id].get('status', 'completed')
                if 'error' in status:
                    yield "data: __DONE_WITH_ERRORS__\n\n"
                else:
                    yield "data: __DONE__\n\n"
                break
            # SSE requires escaping newlines
            for line in msg.split('\n'):
                yield f"data: {line}\n\n"
    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


# ===========================================================================
# Entry point
# ===========================================================================
def main():
    port = 5000
    print(f"\n  Demo Hub WDF Lab Instance Prep")
    print(f"  Opening browser at http://localhost:{port}")
    print(f"  Press Ctrl+C to stop.\n")

    # Open browser after a short delay
    threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()

    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)


if __name__ == '__main__':
    main()
