#!/usr/bin/env python3
"""Preview-only test for the consolidated update set on a fresh instance."""

import os
import sys
import time
import re
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
CONSOLIDATED_XML = os.path.join(BASE_DIR, 'consolidated', 'WDF_Lab_Consolidated.xml')
LOG_DIR = os.path.join(SCRIPT_DIR, 'logs')

INSTANCE = os.environ.get('SN_INSTANCE', 'https://demoalectriallwfza142083.service-now.com')
USERNAME = os.environ.get('SN_USER', 'admin')
PASSWORD = os.environ.get('SN_PASS', '')


def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    if hasattr(log, 'fh'):
        log.fh.write(line + '\n')
        log.fh.flush()


def main():
    if not PASSWORD:
        print("ERROR: Set SN_PASS environment variable")
        sys.exit(1)

    if not os.path.exists(CONSOLIDATED_XML):
        print(f"ERROR: {CONSOLIDATED_XML} not found. Run merge_update_sets.py first.")
        sys.exit(1)

    # Setup log file
    os.makedirs(LOG_DIR, exist_ok=True)
    hostname = INSTANCE.replace('https://', '').replace('http://', '').split('.')[0]
    log_file = os.path.join(LOG_DIR,
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_preview_{hostname}.log")
    log.fh = open(log_file, 'w')
    log(f"Preview Test — {INSTANCE}")
    log(f"Log file: {log_file}")

    # --- Login ---
    ui = requests.Session()
    api = requests.Session()
    api.auth = (USERNAME, PASSWORD)
    api.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    log("Logging in...")
    ui.post(f'{INSTANCE}/login.do', data={
        'user_name': USERNAME, 'user_password': PASSWORD,
        'sys_action': 'sysverb_login'
    }, allow_redirects=True, timeout=120)

    ck = ''
    for attempt in range(3):
        resp = ui.get(f'{INSTANCE}/sys.scripts.do', timeout=60)
        m = re.search(r"g_ck\s*=\s*'([^']+)'", resp.text)
        if not m:
            m = re.search(r"var CK = '([^']+)'", resp.text)
        if not m:
            m = re.search(r'name="sysparm_ck"[^>]*value="([^"]+)"', resp.text)
        ck = m.group(1) if m else ''
        if ck:
            break
        log(f"  CK attempt {attempt+1}/3 failed, retrying...")
        import time as _t; _t.sleep(3)
    if ck:
        log("  Login OK")
    else:
        log("  WARNING: No CK token — upload may fail")

    # --- Upload ---
    fname = os.path.basename(CONSOLIDATED_XML)
    log(f"Uploading {fname} ({os.path.getsize(CONSOLIDATED_XML)/1024/1024:.1f} MB)...")
    with open(CONSOLIDATED_XML, 'rb') as f:
        resp = ui.post(f'{INSTANCE}/sys_upload.do',
            data={
                'sysparm_ck': ck,
                'sysparm_referring_url': 'sys_remote_update_set_list.do',
                'sysparm_target': 'sys_remote_update_set',
            },
            files={'attachFile': (fname, f, 'application/xml')},
            allow_redirects=False, timeout=600)
    if resp.status_code in [200, 301, 302, 303]:
        log("  Upload OK")
    else:
        log(f"  Upload FAILED (HTTP {resp.status_code})")
        return

    time.sleep(5)

    # --- Find uploaded update set ---
    log("Finding uploaded batch parent...")
    r = api.get(f'{INSTANCE}/api/now/table/sys_remote_update_set', params={
        'sysparm_query': 'name=WDF Lab Consolidated - Batch Parent^ORDERBYDESCsys_created_on',
        'sysparm_fields': 'sys_id,name,state',
        'sysparm_limit': '1'
    })
    results = r.json().get('result', [])
    if not results:
        log("  ERROR: Could not find uploaded update set")
        return
    parent = results[0]
    sys_id = parent['sys_id']
    log(f"  Found: {parent['name']} (sys_id={sys_id}, state={parent['state']})")

    # --- Preview (batch) ---
    log("Starting batch preview...")
    script = f"""
var gr = new GlideRecord('sys_remote_update_set');
if (gr.get('{sys_id}')) {{
    gr.state = 'previewing';
    gr.update();
    var worker = new GlideScriptedHierarchicalWorker();
    worker.setProgressName('Batch Preview for: ' + gr.name);
    worker.setScriptIncludeName('UpdateSetPreviewer');
    worker.setScriptIncludeMethod('generateForHierarchy');
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
    resp = ui.post(f'{INSTANCE}/sys.scripts.do', data={
        'sysparm_ck': ck, 'script': script,
        'runscript': 'Run script', 'quota_managed_transaction': 'on',
    }, timeout=180)
    body = re.sub(r'<[^>]+>', ' ', resp.text)
    body = re.sub(r'\s+', ' ', body).strip()
    idx = body.find('Script:')
    output = body[idx:idx+400].strip() if idx >= 0 else ''
    log(f"  {output}")

    # --- Wait for preview to complete ---
    log("Waiting for preview to complete...")
    start = time.time()
    last_log = 0
    final_state = None
    while time.time() - start < 900:  # 15 min timeout
        time.sleep(10)
        r = api.get(f'{INSTANCE}/api/now/table/sys_remote_update_set/{sys_id}',
                    params={'sysparm_fields': 'state,name'})
        if r.status_code == 200:
            info = r.json().get('result', {})
            state = info.get('state', '')
            elapsed = int(time.time() - start)
            if state in ['previewed', 'committed']:
                log(f"  Preview done! state={state} ({elapsed}s)")
                final_state = state
                break
            if elapsed - last_log >= 30:
                log(f"  Waiting... state={state} ({elapsed}s)")
                last_log = elapsed

    if not final_state:
        log("  Preview timed out!")
        return

    # --- Collect preview problems ---
    log("\n=== PREVIEW PROBLEM ANALYSIS ===")

    # Get all children
    r = api.get(f'{INSTANCE}/api/now/table/sys_remote_update_set', params={
        'sysparm_query': f'remote_base_update_set={sys_id}',
        'sysparm_fields': 'sys_id,name,state',
        'sysparm_limit': '50'
    })
    children = r.json().get('result', [])
    ids_to_check = [{'sys_id': sys_id, 'name': 'Batch Parent'}]
    for c in children:
        ids_to_check.append(c)
    log(f"Checking {len(ids_to_check)} update sets for preview problems...\n")

    all_problems = []
    for us in ids_to_check:
        us_id = us['sys_id']
        us_name = us.get('name', us_id)
        r = api.get(f'{INSTANCE}/api/now/table/sys_update_preview_problem', params={
            'sysparm_query': f'remote_update_set={us_id}',
            'sysparm_fields': 'sys_id,type,description,status',
            'sysparm_limit': '500'
        })
        problems = r.json().get('result', [])
        if problems:
            log(f"--- {us_name}: {len(problems)} problems ---")
            for p in problems:
                all_problems.append({
                    'update_set': us_name,
                    'type': p.get('type', ''),
                    'description': p.get('description', ''),
                    'status': p.get('status', ''),
                })
                log(f"  [{p.get('type','')}] {p.get('description','')[:200]}")
        else:
            log(f"--- {us_name}: 0 problems ---")

    # --- Summary ---
    log(f"\n=== SUMMARY ===")
    log(f"Total preview problems: {len(all_problems)}")

    # Group by type
    by_type = {}
    for p in all_problems:
        t = p['type']
        by_type.setdefault(t, []).append(p)
    for t, items in sorted(by_type.items()):
        log(f"  {t}: {len(items)}")

    # Group by description pattern
    log(f"\nProblem patterns:")
    patterns = {}
    for p in all_problems:
        desc = p['description']
        # Normalize: remove sys_ids and specific names
        key = re.sub(r'[0-9a-f]{32}', '<id>', desc)
        key = re.sub(r"'[^']*'", "'...'", key)
        patterns.setdefault(key, []).append(p)
    for pat, items in sorted(patterns.items(), key=lambda x: -len(x[1])):
        log(f"  [{len(items)}x] {pat[:200]}")

    log(f"\nLog saved to: {log_file}")
    log.fh.close()


if __name__ == '__main__':
    main()
