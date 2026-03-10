#!/usr/bin/env python3
"""
merge_update_sets.py

Consolidates 21 update set XMLs and 7 XML unload files into a single
ServiceNow batch-parent update set XML with scoped children.

Structure:
  - Batch Parent (global)
    - Child 1: sn_erp_integration  (Zero Copy for ERP)
    - Child 2: x_snc_alectri_zc_0  (Alectri ZCC Simulator)
    - Child 3: x_snc_forecast_v_0  (Forecast Variance)
    - Child 4: global              (everything else + XML unload data)

Records are routed to children by their <application> scope ID.
This ensures scopes are created before records that reference them,
and prevents scope mismatch errors.

Usage:
    python3 merge_update_sets.py

Output:
    internal-demo-hub/consolidated/WDF_Lab_Consolidated.xml
"""

import os
import re
import sys
import uuid
import hashlib
import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # internal-demo-hub/
UPDATE_SET_DIR = os.path.join(BASE_DIR, 'update_sets')
XML_UNLOAD_DIR = os.path.join(BASE_DIR, 'xml_unloads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'consolidated')

BATCH_NAME = 'WDF Lab Consolidated - Batch Parent'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def _make_sys_id(seed):
    """Generate a deterministic 32-char hex ID from a seed string."""
    return hashlib.md5(seed.encode()).hexdigest()


# Skip patterns: sys_update_name containing any of these -> strip
SKIP_PATTERNS = [
    'df_variance_baseline_v',    # stale data fabric table + all fields
    'expense_stream',            # stale/renamed table
    'u_cmdb_qb_result_',         # CMDB query builder temp tables
    'forecast_variance_mapping_table',  # old table (ACL deletes)
    'forecast_variance_link_test',      # stale test table
    'x_snc_forecast_v_0_df_test',       # stale test table
    'u_imp_tmpl_',                      # import template tables (don't exist on fresh)
]

# Records with DELETE action whose name contains these patterns -> strip
# These are old column/table deletes that fail on fresh instances
DELETE_SKIP_PATTERNS = [
    'x_snc_forecast_v_0_expense_transactions_u_',  # old u_ custom columns
    'x_snc_forecast_v_0_expense_transactions_null', # old ui_list for table
]

# Specific sys_update_name values to always skip (platform records captured accidentally)
EXACT_SKIP_NAMES = {
    'sn_aia_skill_metadata_d254b5ea3b7a3a5062f31831a3e45ab7',  # AP GenAI "Invoice resolution provider" (platform)
    'sn_aia_team_member_f064fdea3b7a3a5062f31831a3e45a9c',     # AP GenAI team member (platform)
}

# ---------------------------------------------------------------------------
# Batch children definition (order matters — scopes created first)
# ---------------------------------------------------------------------------
CHILDREN = [
    {
        'key': 'sn_erp_integration',
        'name': 'WDF Lab - Zero Copy for ERP',
        'app_display': 'Zero Copy Connector for ERP',
        'app_id': '5e4866a16f2111100e6ee0d0245b3610',
        'app_scope': 'sn_erp_integration',
        'app_version': '8.0.14',
        'scope_ids': {'5e4866a16f2111100e6ee0d0245b3610'},
    },
    {
        'key': 'x_snc_alectri_zc_0',
        'name': 'WDF Lab - Alectri ZCC Simulator',
        'app_display': 'Alectri ZCC Simulator',
        'app_id': '1556bceb93d27e1073ecfd5da503d6b6',
        'app_scope': 'x_snc_alectri_zc_0',
        'app_version': '1.0.1',
        'scope_ids': {'1556bceb93d27e1073ecfd5da503d6b6'},
    },
    {
        'key': 'x_snc_forecast_v_0',
        'name': 'WDF Lab - Forecast Variance',
        'app_display': 'Forecast Variance',
        'app_id': 'a4fd2da13bf8be5062f31831a3e45ac9',
        'app_scope': 'x_snc_forecast_v_0',
        'app_version': '1.3.0',
        'scope_ids': {'a4fd2da13bf8be5062f31831a3e45ac9'},
    },
    {
        'key': 'global',
        'name': 'WDF Lab - Global',
        'app_display': 'Global',
        'app_id': 'global',
        'app_scope': 'global',
        'app_version': '',
        'scope_ids': set(),  # catch-all for everything else
    },
]

# Pre-compute sys_ids for batch parent and children
PARENT_SYS_ID = _make_sys_id(f'{BATCH_NAME}_parent')
PARENT_REMOTE_SYS_ID = _make_sys_id(f'{BATCH_NAME}_remote')

for child in CHILDREN:
    child['sys_id'] = _make_sys_id(f'{child["name"]}_child')
    child['remote_sys_id'] = _make_sys_id(f'{child["name"]}_remote')

# Build scope_id -> child lookup (scoped children only)
SCOPE_TO_CHILD = {}
for child in CHILDREN:
    for sid in child['scope_ids']:
        SCOPE_TO_CHILD[sid] = child
GLOBAL_CHILD = CHILDREN[-1]  # catch-all


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def numeric_sort_key(filepath):
    basename = os.path.basename(filepath)
    m = re.match(r'(\d+)', basename)
    return int(m.group(1)) if m else 999


ACTION_RE = re.compile(r'<action>(.*?)</action>')


def should_skip(name, block=None):
    """Check if a sys_update_xml record should be skipped.
    Checks the name field first, then optionally checks the full block
    content (including payload) to catch records like ais_datasource that
    reference stale tables in their payload but not in their name."""
    if name in EXACT_SKIP_NAMES:
        return True
    check_str = name.lower()
    for pattern in SKIP_PATTERNS:
        if pattern.lower() in check_str:
            return True
    if block:
        block_lower = block.lower()
        for pattern in SKIP_PATTERNS:
            if pattern.lower() in block_lower:
                return True
        # Skip DELETE actions on old custom columns
        action_match = ACTION_RE.search(block)
        if action_match and 'DELETE' in action_match.group(1):
            for pattern in DELETE_SKIP_PATTERNS:
                if pattern.lower() in check_str:
                    return True
    return False


def get_child_for_scope(scope_id):
    """Route a record to the correct batch child based on its application scope."""
    return SCOPE_TO_CHILD.get(scope_id, GLOBAL_CHILD)


def discover_update_sets():
    if not os.path.isdir(UPDATE_SET_DIR):
        return []
    return sorted(glob.glob(os.path.join(UPDATE_SET_DIR, "*.xml")),
                  key=numeric_sort_key)


def discover_xml_unloads():
    if not os.path.isdir(XML_UNLOAD_DIR):
        return []
    files = sorted(glob.glob(os.path.join(XML_UNLOAD_DIR, "*.xml")),
                   key=numeric_sort_key)
    result = []
    for f in files:
        basename = os.path.basename(f)
        parts = basename.split('_', 1)
        if len(parts) == 2:
            table = parts[1].replace('.xml', '')
        else:
            table = basename.replace('.xml', '')
        result.append({'file': f, 'table': table})
    return result


# ---------------------------------------------------------------------------
# Extract sys_update_xml blocks from update set files (string-based)
# ---------------------------------------------------------------------------
BLOCK_RE = re.compile(
    r'(<sys_update_xml\b[^>]*>.*?</sys_update_xml>)',
    re.DOTALL
)
NAME_RE = re.compile(r'<name>(.*?)</name>')
APP_RE = re.compile(r'<application\s+display_value="[^"]*">([^<]+)</application>')
REMOTE_US_RE = re.compile(
    r'<remote_update_set[^>]*>.*?</remote_update_set>',
    re.DOTALL
)
APP_REWRITE_RE = re.compile(
    r'<application\s+display_value="[^"]*">[^<]+</application>'
)


def extract_records_from_update_set(xml_file):
    """Extract sys_update_xml blocks as raw strings from an update set XML.
    Returns list of (name, app_scope_id, raw_block_string) tuples."""
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    records = []
    for match in BLOCK_RE.finditer(content):
        block = match.group(1)
        name_match = NAME_RE.search(block)
        name = name_match.group(1) if name_match else ''
        app_match = APP_RE.search(block)
        app_id = app_match.group(1) if app_match else 'global'
        records.append((name, app_id, block))

    return records


def rewrite_remote_update_set(block, child):
    """Replace the remote_update_set reference to point to the correct child."""
    new_ref = (f'<remote_update_set display_value="{child["name"]}">'
               f'{child["sys_id"]}</remote_update_set>')
    return REMOTE_US_RE.sub(new_ref, block)


def rewrite_application_to_global(block):
    """Rewrite the <application> field to global to avoid scope mismatch
    errors for records routed to the Global child."""
    return APP_REWRITE_RE.sub(
        '<application display_value="Global">global</application>', block, count=1)


# ---------------------------------------------------------------------------
# Wrap XML unload records as sys_update_xml entries
# ---------------------------------------------------------------------------
def wrap_xml_unload_records(xml_file, table):
    """Parse an XML unload file and wrap each record as a sys_update_xml block.
    All XML unload records go to the global child.
    Returns list of (name, app_scope_id, block_string) tuples."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    child = GLOBAL_CHILD

    records = []
    for record in root:
        sid_el = record.find('sys_id')
        sid = sid_el.text if sid_el is not None and sid_el.text else str(uuid.uuid4()).replace('-', '')

        name_el = record.find('name') or record.find('sys_name')
        target_name = name_el.text if name_el is not None and name_el.text else sid

        update_name = f'{table}_{sid}'

        record_str = ET.tostring(record, encoding='unicode')

        payload_inner = (f'<?xml version="1.0" encoding="UTF-8"?>'
                         f'<record_update table="{table}">'
                         f'{record_str}'
                         f'</record_update>')

        payload_escaped = (payload_inner
                           .replace('&', '&amp;')
                           .replace('<', '&lt;')
                           .replace('>', '&gt;')
                           .replace('"', '&quot;'))

        record_sys_id = _make_sys_id(f'xml_unload_{table}_{sid}')

        block = f"""<sys_update_xml action="INSERT_OR_UPDATE">
<action>INSERT_OR_UPDATE</action>
<application display_value="{child['app_display']}">{child['app_id']}</application>
<category>customer</category>
<comments />
<name>{update_name}</name>
<payload>{payload_escaped}</payload>
<payload_hash>0</payload_hash>
<remote_update_set display_value="{child['name']}">{child['sys_id']}</remote_update_set>
<replace_on_upgrade>false</replace_on_upgrade>
<sys_class_name>sys_update_xml</sys_class_name>
<sys_created_by>admin</sys_created_by>
<sys_created_on>{NOW}</sys_created_on>
<sys_id>{record_sys_id}</sys_id>
<sys_mod_count>0</sys_mod_count>
<sys_recorded_at>0</sys_recorded_at>
<sys_updated_by>admin</sys_updated_by>
<sys_updated_on>{NOW}</sys_updated_on>
<table>{table}</table>
<target_name>{target_name}</target_name>
<type>INSERT_OR_UPDATE</type>
<update_domain>global</update_domain>
<update_guid>{record_sys_id}</update_guid>
<update_guid_history>{record_sys_id}</update_guid_history>
<update_set />
<view />
</sys_update_xml>"""
        records.append((update_name, 'global', block))

    return records


# ---------------------------------------------------------------------------
# Build batch parent XML structure
# ---------------------------------------------------------------------------
def build_batch_parent_xml():
    """Build the batch parent sys_remote_update_set header."""
    return f"""<sys_remote_update_set action="INSERT_OR_UPDATE">
<application display_value="Global">global</application>
<application_name>Global</application_name>
<application_scope>global</application_scope>
<application_version />
<collisions />
<commit_date />
<deleted />
<description>Consolidated batch update set for WDF TypeA Lab. Contains all 21 update sets and 7 XML unloads with scoped children.</description>
<inserted />
<name>{BATCH_NAME}</name>
<origin_sys_id>{_make_sys_id(BATCH_NAME + '_origin')}</origin_sys_id>
<parent display_value="" />
<release_date />
<remote_base_update_set display_value="{BATCH_NAME}">{PARENT_SYS_ID}</remote_base_update_set>
<remote_parent_id />
<remote_sys_id>{PARENT_REMOTE_SYS_ID}</remote_sys_id>
<state>loaded</state>
<summary />
<sys_class_name>sys_remote_update_set</sys_class_name>
<sys_created_by>admin</sys_created_by>
<sys_created_on>{NOW}</sys_created_on>
<sys_id>{PARENT_SYS_ID}</sys_id>
<sys_mod_count>1</sys_mod_count>
<sys_updated_by>admin</sys_updated_by>
<sys_updated_on>{NOW}</sys_updated_on>
<update_set display_value="" />
<update_source display_value="" />
<updated />
</sys_remote_update_set>
"""


def build_child_xml(child):
    """Build a child sys_remote_update_set entry."""
    return f"""<sys_remote_update_set action="INSERT_OR_UPDATE">
<application display_value="{child['app_display']}">{child['app_id']}</application>
<application_name>{child['app_display']}</application_name>
<application_scope>{child['app_scope']}</application_scope>
<application_version>{child['app_version']}</application_version>
<collisions />
<commit_date />
<deleted />
<description>Child of {BATCH_NAME}</description>
<inserted />
<name>{child['name']}</name>
<origin_sys_id />
<parent display_value="{BATCH_NAME}">{PARENT_SYS_ID}</parent>
<release_date />
<remote_base_update_set display_value="{BATCH_NAME}">{PARENT_SYS_ID}</remote_base_update_set>
<remote_parent_id />
<remote_sys_id>{child['remote_sys_id']}</remote_sys_id>
<state>in_hierarchy</state>
<summary />
<sys_class_name>sys_remote_update_set</sys_class_name>
<sys_created_by>admin</sys_created_by>
<sys_created_on>{NOW}</sys_created_on>
<sys_id>{child['sys_id']}</sys_id>
<sys_mod_count>0</sys_mod_count>
<sys_updated_by>admin</sys_updated_by>
<sys_updated_on>{NOW}</sys_updated_on>
<update_set display_value="" />
<update_source display_value="" />
<updated />
</sys_remote_update_set>
"""


def main():
    print(f"Merge Update Sets — {BATCH_NAME}")
    print(f"=" * 60)

    # Buckets: child_key -> list of (source_file, name, block)
    buckets = {child['key']: [] for child in CHILDREN}
    skipped = []

    # Phase 1: Update Sets
    us_files = discover_update_sets()
    print(f"\nPhase 1: Found {len(us_files)} update set files.")

    for xml_file in us_files:
        fname = os.path.basename(xml_file)
        records = extract_records_from_update_set(xml_file)
        kept = 0
        skip_count = 0
        for name, app_id, block in records:
            if should_skip(name, block):
                skipped.append((fname, name, 'skip_pattern'))
                skip_count += 1
            else:
                child = get_child_for_scope(app_id)
                block = rewrite_remote_update_set(block, child)
                if child['key'] == 'global' and app_id != 'global':
                    block = rewrite_application_to_global(block)
                buckets[child['key']].append((fname, name, block))
                kept += 1
        print(f"  {fname}: {kept} kept, {skip_count} skipped")

    # Phase 2: XML Unloads
    unload_tasks = discover_xml_unloads()
    print(f"\nPhase 2: Found {len(unload_tasks)} XML unload files.")

    for task in unload_tasks:
        fname = os.path.basename(task['file'])
        table = task['table']
        records = wrap_xml_unload_records(task['file'], table)
        kept = 0
        for name, app_id, block in records:
            if should_skip(name):
                skipped.append((fname, name, 'skip_pattern'))
            else:
                buckets[GLOBAL_CHILD['key']].append((fname, name, block))
                kept += 1
        print(f"  {fname} ({table}): {kept} records")

    # Deduplicate within each bucket: keep last occurrence per sys_update_name
    total_before = sum(len(b) for b in buckets.values())
    for key in buckets:
        seen = {}
        for i, (source, name, block) in enumerate(buckets[key]):
            seen[name] = i
        dedup_indices = set(seen.values())
        buckets[key] = [buckets[key][i] for i in sorted(dedup_indices)]

    total_after = sum(len(b) for b in buckets.values())
    dedup_count = total_before - total_after

    # Summary
    print(f"\n--- Summary ---")
    print(f"Total records extracted:  {total_before + len(skipped)}")
    print(f"Skipped (skip list):      {len(skipped)}")
    print(f"Duplicates removed:       {dedup_count}")
    print(f"Final record count:       {total_after}")
    for child in CHILDREN:
        print(f"  {child['name']}: {len(buckets[child['key']])} records")

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, 'WDF_Lab_Consolidated.xml')

    print(f"\nWriting {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"<?xml version='1.0' encoding='UTF-8'?>\n")
        out.write(f'<unload unload_date="{NOW}">\n')

        # Batch parent header
        out.write(build_batch_parent_xml())

        # Child headers (all children, even empty ones)
        for child in CHILDREN:
            out.write(build_child_xml(child))

        # Records per child (in child order)
        for child in CHILDREN:
            for source, name, block in buckets[child['key']]:
                out.write(block)
                out.write('\n')

        out.write('</unload>\n')

    file_size = os.path.getsize(output_path)
    print(f"Done! File size: {file_size / 1024 / 1024:.1f} MB")

    # Write skip report
    report_path = os.path.join(OUTPUT_DIR, 'skip_report.txt')
    with open(report_path, 'w') as rpt:
        rpt.write(f"Skip Report — {BATCH_NAME}\n")
        rpt.write(f"Generated: {NOW}\n")
        rpt.write(f"{'=' * 60}\n\n")
        rpt.write(f"Skip patterns:\n")
        for p in SKIP_PATTERNS:
            rpt.write(f"  - {p}\n")
        rpt.write(f"\nBatch children:\n")
        for child in CHILDREN:
            rpt.write(f"  - {child['name']} ({child['app_scope']}): "
                       f"{len(buckets[child['key']])} records\n")
        rpt.write(f"\nSkipped records ({len(skipped)}):\n")
        for source, name, reason in skipped:
            rpt.write(f"  [{reason}] {source} :: {name}\n")
        rpt.write(f"\nDuplicates removed: {dedup_count}\n")
        rpt.write(f"Final record count: {total_after}\n")

    print(f"Skip report: {report_path}")


if __name__ == '__main__':
    main()
