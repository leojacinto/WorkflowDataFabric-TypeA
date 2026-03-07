# Demo Hub WDF Lab — Instance Prep Instructions

---

## Important Stuff — Execute for Lab if You Are Using a Demo Hub Instance

### What This Does

This tool automatically imports all the required update sets and data into your ServiceNow Demo Hub instance so it's ready for the WDF (Workflow Data Fabric) lab exercises. Instead of manually uploading and committing 20+ files one by one, this tool does it all for you in one click.

### Download

📦 **[Download the Instance Prep Tool (ZIP)](downloads/demo-hub-wdf-lab-instance-prep.zip)**

### Step-by-Step Instructions

1. **Download** the ZIP file using the link above (click "Download raw file" on GitHub)
2. **Unzip** the file — you will see a folder called `demo-hub-wdf-lab-instance-prep`
3. **Open the folder** and find the launcher for your operating system:
   - **Mac/Linux:** Double-click `demo-hub-wdf-lab-instance-prep.sh`
     - If it doesn't open, right-click → Open With → Terminal
     - Or open Terminal, drag the file into it, and press Enter
   - **Windows:** Double-click `demo-hub-wdf-lab-instance-prep.bat`
4. **Wait for setup** — On first run, it will install Python dependencies automatically (~30 seconds)
5. **Your browser will open** with a form. Fill in:
   - **Instance Name** — Just the name part, e.g. if your URL is `https://myinstance.service-now.com`, enter `myinstance`
   - **Username** — Your ServiceNow username (e.g. `admin`)
   - **Password** — Your ServiceNow password
6. **Click "Start Instance Prep"** and watch the progress in the log area
7. **Wait for completion** — This typically takes 15-30 minutes depending on the number of update sets
8. **Done!** Once you see "Completed!" you can close the browser and the terminal

### About Your Password

🔒 **Your password is safe.** The tool runs entirely on your local machine. Your password is:
- Used **in-memory only** to connect directly to your ServiceNow instance
- **Never stored** to disk, to a file, to a log, or anywhere else
- **Never transmitted** to any server other than your own ServiceNow instance
- **Discarded** the moment the tool finishes or you close it

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python 3 is not installed" | The script will try to install it automatically. If it fails, install Python from [python.org/downloads](https://www.python.org/downloads/) and re-run. |
| Browser doesn't open | Manually open `http://localhost:5000` in your browser. |
| "Failed to connect" error | Check your instance name is correct (just the name, not the full URL). Make sure your instance is awake (not hibernating). |
| Login fails | Verify your username and password. Try logging into your instance in a browser first to confirm. |
| A file fails to import | The tool retries 3 times per file. If it still fails, note the filename from the log and ask your lab instructor for help. |
| Script won't run on Mac | Open Terminal and run: `chmod +x demo-hub-wdf-lab-instance-prep.sh` then `./demo-hub-wdf-lab-instance-prep.sh` |

### Need Help?

If you can't get the tool to work, ask your lab instructor to use the **Multi Instance (Admin)** tab to run the import for you. They just need your instance name and credentials.

---

## Technical Stuff — If You Want to Know How the Program Works

### Architecture

The tool is a single-file Python/Flask web application (`demo_hub_prep.py`) that:

1. Starts a local web server on `http://localhost:5000`
2. Opens your default browser to the web UI
3. Accepts your ServiceNow instance name + credentials via the form
4. Runs the import pipeline in a background thread
5. Streams real-time progress back to the browser via Server-Sent Events (SSE)

### Import Pipeline

For each update set XML file in the `update_sets/` directory, the tool executes:

1. **Upload** — Posts the XML file to `sys_upload.do` using a cookie-based browser session (same as manual upload)
2. **Preview** — Triggers the update set preview via a background script on `sys.scripts.do`
3. **Accept Errors** — Automatically accepts all preview problems/conflicts via the REST API
4. **Commit** — Triggers the update set commit via background script
5. **Verify** — Polls the update set state until it reaches `committed`

For XML unload files in `xml_unloads/`, the tool uploads them directly to their target tables via `sys_upload.do`.

### Batch (Hierarchy) Update Sets

The tool automatically detects batch/hierarchy update sets (XML files containing multiple `sys_remote_update_set` records) and uses the appropriate ServiceNow APIs:
- `UpdateSetPreviewer.generateForHierarchy()` for preview
- `SNC.HierarchyUpdateSetScriptable.commitHierarchy()` for commit

### File Naming Convention

**Update Sets** (`update_sets/` directory):
- Files are processed in alphabetical/sorted order
- Prefix with numbers for ordering: `01_name.xml`, `02_name.xml`, etc.

**XML Unloads** (`xml_unloads/` directory):
- Filename format: `NN_table_name.xml` (e.g. `01_sn_erp_integration_cost_center.xml`)
- The table name is extracted from the filename (everything after the first `_` and before `.xml`)
- The numeric prefix controls processing order

### Retry Logic

- **Login:** 3 retries with 10s delay
- **Upload:** 3 retries with re-login between attempts
- **Background scripts:** 3 retries with re-login
- **State polling:** Checks every 5s, times out after 600s (10 minutes)

### Multi-Instance Mode

The **Multi Instance (Admin)** tab allows running the same import across multiple instances. Instances are processed sequentially (not in parallel) to avoid overwhelming the local machine. Each instance gets its own `SNClient` session with independent authentication.

### Directory Structure

```
demo-hub-wdf-lab-instance-prep/
├── demo-hub-wdf-lab-instance-prep.sh   # Mac/Linux launcher
├── demo-hub-wdf-lab-instance-prep.bat  # Windows launcher
├── demo_hub_prep.py                     # Main application
├── requirements.txt                     # Python dependencies (flask, requests)
├── update_sets/                         # Update set XML files (processed in order)
│   ├── 01_zero_copy_for_erp.xml
│   ├── 02_zcc_simulator_batch_parent.xml
│   └── ...
└── xml_unloads/                         # XML unload files (NN_table_name.xml)
    ├── 01_sn_erp_integration_cost_center.xml
    └── ...
```

### Dependencies

- **Python 3.8+** (auto-installed by launcher scripts if missing)
- **Flask** — Local web server and UI
- **Requests** — HTTP client for ServiceNow API calls

### Security Notes

- Credentials are held in Python variables (RAM) for the duration of the session only
- No credentials are written to any file, log, or database
- The Flask server binds to `127.0.0.1` (localhost only) — not accessible from other machines
- All communication with ServiceNow uses HTTPS
- Virtual environment is created locally (`.venv/`) to avoid polluting system Python
