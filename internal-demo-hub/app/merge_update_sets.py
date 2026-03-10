#!/usr/bin/env python3
"""
merge_update_sets.py

Consolidates 21 update set XMLs and 7 XML unload files into a single
global-scope ServiceNow update set XML.  Applies a skip list to remove
records that would cause preview problems on a fresh instance.

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

CONSOLIDATED_NAME = 'WDF Lab Consolidated'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def _make_sys_id(seed):
    """Generate a deterministic 32-char hex ID from a seed string."""
    return hashlib.md5(seed.encode()).hexdigest()


REMOTE_US_SYS_ID = _make_sys_id(f'{CONSOLIDATED_NAME}_remote_update_set')
UPDATE_SET_SYS_ID = _make_sys_id(f'{CONSOLIDATED_NAME}_update_set')

# Skip patterns: sys_update_name containing any of these -> strip
SKIP_PATTERNS = [
    'df_variance_baseline_v',    # stale data fabric table + all fields
    'expense_stream',            # stale/renamed table
    'u_cmdb_qb_result_',         # CMDB query builder temp tables
    'forecast_variance_mapping_table',  # old table (ACL deletes)
]

# Scope mapping for XML unload tables
SCOPE_MAP = {
    'sn_erp_integration_cost_center': ('Zero Copy Connector for ERP',
                                        '5e4866a16f2111100e6ee0d0245b3610',
                                        'sn_erp_integration'),
    'x_snc_forecast_v_0_variance_task': ('Forecast Variance',
                                          'a4fd2da13bf8be5062f31831a3e45ac9',
                                          'x_snc_forecast_v_0'),
    'x_snc_forecast_v_0_expense_transactions': ('Forecast Variance',
                                                 'a4fd2da13bf8be5062f31831a3e45ac9',
                                                 'x_snc_forecast_v_0'),
    'x_snc_forecast_v_0_cost_center_budget_history': ('Forecast Variance',
                                                       'a4fd2da13bf8be5062f31831a3e45ac9',
                                                       'x_snc_forecast_v_0'),
    'x_snc_forecast_v_0_expense_transaction_event': ('Forecast Variance',
                                                      'a4fd2da13bf8be5062f31831a3e45ac9',
                                                      'x_snc_forecast_v_0'),
    'u_cc_summary': ('Global', 'global', 'global'),
    'x_snc_alectri_zc_0_source_databases': ('Alectri ZCC Simulator cLabs',
                                             'dba6b91b3b1ff29062f31831a3e45a8a',
                                             'x_snc_alectri_zc_0'),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def numeric_sort_key(filepath):
    basename = os.path.basename(filepath)
    m = re.match(r'(\d+)', basename)
    return int(m.group(1)) if m else 999


def should_skip(name):
    """Check if a sys_update_xml record should be skipped based on its name."""
    name_lower = name.lower()
    for pattern in SKIP_PATTERNS:
        if pattern.lower() in name_lower:
            return True
    return False


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
# Regex to extract <sys_update_xml ...>...</sys_update_xml> blocks
BLOCK_RE = re.compile(
    r'(<sys_update_xml\b[^>]*>.*?</sys_update_xml>)',
    re.DOTALL
)

# Regex to extract <name>...</name> from within a block
NAME_RE = re.compile(r'<name>(.*?)</name>')

# Regex to replace <remote_update_set ...>...</remote_update_set>
REMOTE_US_RE = re.compile(
    r'<remote_update_set[^>]*>.*?</remote_update_set>',
    re.DOTALL
)


def extract_records_from_update_set(xml_file):
    """Extract sys_update_xml blocks as raw strings from an update set XML.
    Returns list of (name, raw_block_string) tuples."""
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    records = []
    for match in BLOCK_RE.finditer(content):
        block = match.group(1)
        # Extract name
        name_match = NAME_RE.search(block)
        name = name_match.group(1) if name_match else ''
        records.append((name, block))

    return records


def rewrite_remote_update_set(block):
    """Replace the remote_update_set reference in a block to point to our
    consolidated update set."""
    new_ref = (f'<remote_update_set display_value="{CONSOLIDATED_NAME}">'
               f'{REMOTE_US_SYS_ID}</remote_update_set>')
    return REMOTE_US_RE.sub(new_ref, block)


# ---------------------------------------------------------------------------
# Wrap XML unload records as sys_update_xml entries
# ---------------------------------------------------------------------------
def wrap_xml_unload_records(xml_file, table):
    """Parse an XML unload file and wrap each record as a sys_update_xml block.
    Returns list of (name, block_string) tuples."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    scope_info = SCOPE_MAP.get(table, ('Global', 'global', 'global'))
    app_display, app_id, app_scope = scope_info

    records = []
    for record in root:
        # Get sys_id
        sid_el = record.find('sys_id')
        sid = sid_el.text if sid_el is not None and sid_el.text else str(uuid.uuid4()).replace('-', '')

        # Get sys_name or name for target_name
        name_el = record.find('name') or record.find('sys_name')
        target_name = name_el.text if name_el is not None and name_el.text else sid

        update_name = f'{table}_{sid}'

        # Serialize the record to string for payload
        record_str = ET.tostring(record, encoding='unicode')

        # Wrap in record_update
        payload_inner = (f'<?xml version="1.0" encoding="UTF-8"?>'
                         f'<record_update table="{table}">'
                         f'{record_str}'
                         f'</record_update>')

        # Escape for XML embedding (not CDATA — use entity encoding to match
        # existing update set style)
        payload_escaped = (payload_inner
                           .replace('&', '&amp;')
                           .replace('<', '&lt;')
                           .replace('>', '&gt;')
                           .replace('"', '&quot;'))

        # Generate a unique sys_id for this sys_update_xml record
        record_sys_id = _make_sys_id(f'xml_unload_{table}_{sid}')

        block = f"""<sys_update_xml action="INSERT_OR_UPDATE">
<action>INSERT_OR_UPDATE</action>
<application display_value="{app_display}">{app_id}</application>
<category>customer</category>
<comments />
<name>{update_name}</name>
<payload>{payload_escaped}</payload>
<payload_hash>0</payload_hash>
<remote_update_set display_value="{CONSOLIDATED_NAME}">{REMOTE_US_SYS_ID}</remote_update_set>
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
        records.append((update_name, block))

    return records


# ---------------------------------------------------------------------------
# Build consolidated XML
# ---------------------------------------------------------------------------
def build_consolidated_header():
    """Build the sys_remote_update_set wrapper (global scope)."""
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<unload unload_date="{NOW}">
<sys_remote_update_set action="INSERT_OR_UPDATE">
<application display_value="Global">global</application>
<application_name>Global</application_name>
<application_scope>global</application_scope>
<application_version />
<collisions />
<commit_date />
<deleted />
<description>Consolidated update set for WDF TypeA Lab. Contains all 21 update sets and 7 XML unloads merged into a single global-scope update set.</description>
<inserted />
<name>{CONSOLIDATED_NAME}</name>
<origin_sys_id>{_make_sys_id(CONSOLIDATED_NAME + '_origin')}</origin_sys_id>
<parent display_value="" />
<release_date />
<remote_base_update_set display_value="" />
<remote_parent_id />
<remote_sys_id>{UPDATE_SET_SYS_ID}</remote_sys_id>
<state>loaded</state>
<summary />
<sys_class_name>sys_remote_update_set</sys_class_name>
<sys_created_by>admin</sys_created_by>
<sys_created_on>{NOW}</sys_created_on>
<sys_id>{REMOTE_US_SYS_ID}</sys_id>
<sys_mod_count>0</sys_mod_count>
<sys_updated_by>admin</sys_updated_by>
<sys_updated_on>{NOW}</sys_updated_on>
<update_set display_value="" />
<update_source display_value="" />
<updated />
</sys_remote_update_set>
"""


def main():
    print(f"Merge Update Sets — {CONSOLIDATED_NAME}")
    print(f"=" * 60)

    # Collect all records
    all_records = []  # list of (source_file, name, block)
    skipped = []      # list of (source_file, name, reason)

    # Phase 1: Update Sets
    us_files = discover_update_sets()
    print(f"\nFound {len(us_files)} update set files.")

    for xml_file in us_files:
        fname = os.path.basename(xml_file)
        records = extract_records_from_update_set(xml_file)
        kept = 0
        for name, block in records:
            if should_skip(name):
                skipped.append((fname, name, 'skip_pattern'))
            else:
                # Rewrite remote_update_set reference
                block = rewrite_remote_update_set(block)
                all_records.append((fname, name, block))
                kept += 1
        print(f"  {fname}: {kept} kept, {len(records) - kept} skipped")

    # Phase 2: XML Unloads
    unload_tasks = discover_xml_unloads()
    print(f"\nFound {len(unload_tasks)} XML unload files.")

    for task in unload_tasks:
        fname = os.path.basename(task['file'])
        table = task['table']
        records = wrap_xml_unload_records(task['file'], table)
        kept = 0
        for name, block in records:
            if should_skip(name):
                skipped.append((fname, name, 'skip_pattern'))
            else:
                all_records.append((fname, name, block))
                kept += 1
        print(f"  {fname} ({table}): {kept} kept, {len(records) - kept} skipped")

    # Deduplicate: keep last occurrence of each sys_update_name
    seen = {}
    for i, (source, name, block) in enumerate(all_records):
        if name in seen:
            prev_i, prev_source = seen[name]
            # Keep the later one (higher index = later in import order)
            seen[name] = (i, source)
        else:
            seen[name] = (i, source)

    dedup_indices = set(i for i, _ in seen.values())
    dedup_count = len(all_records) - len(dedup_indices)

    print(f"\n--- Summary ---")
    print(f"Total records extracted:  {len(all_records) + len(skipped)}")
    print(f"Skipped (skip list):      {len(skipped)}")
    print(f"Duplicates removed:       {dedup_count}")
    print(f"Final record count:       {len(dedup_indices)}")

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, 'WDF_Lab_Consolidated.xml')

    print(f"\nWriting {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(build_consolidated_header())

        for i, (source, name, block) in enumerate(all_records):
            if i in dedup_indices:
                out.write(block)
                out.write('\n')

        out.write('</unload>\n')

    file_size = os.path.getsize(output_path)
    print(f"Done! File size: {file_size / 1024 / 1024:.1f} MB")

    # Write skip report
    report_path = os.path.join(OUTPUT_DIR, 'skip_report.txt')
    with open(report_path, 'w') as rpt:
        rpt.write(f"Skip Report — {CONSOLIDATED_NAME}\n")
        rpt.write(f"Generated: {NOW}\n")
        rpt.write(f"{'=' * 60}\n\n")
        rpt.write(f"Skip patterns:\n")
        for p in SKIP_PATTERNS:
            rpt.write(f"  - {p}\n")
        rpt.write(f"\nSkipped records ({len(skipped)}):\n")
        for source, name, reason in skipped:
            rpt.write(f"  [{reason}] {source} :: {name}\n")
        rpt.write(f"\nDuplicates removed: {dedup_count}\n")
        rpt.write(f"Final record count: {len(dedup_indices)}\n")

    print(f"Skip report: {report_path}")


if __name__ == '__main__':
    main()
