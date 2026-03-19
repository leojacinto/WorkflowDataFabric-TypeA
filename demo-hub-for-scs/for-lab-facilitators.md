---
icon: person-chalkboard
---

# For Lab Facilitators

This contains considerations for Lab Facilitators.

## Lab Presentation

1. Download the Lab Presentation deck here: [WDF Lab Presentation Deck](https://servicenow-my.sharepoint.com/:p:/r/personal/santosh_panda_servicenow_com/Documents/April%20Workshop/Workflow%20Data%20Fabric%20-%20April.pptx?d=wd8395941af2744fca97f643023af253b\&csf=1\&web=1\&e=HSopWT). This is only accessible through internal ServiceNow login credentials.
2. Familiarize yourself with the presentation guide and modify it as you see fit.
3. Update the Lab URL, QR Codes, and Reservation codes accordingly; use services such as [bitly.com](https://bitly.com) to do this. It is encouraged to shorten URLs and use QR codes to make the experience as seamless for participants as possible.

## Credentials

1. Credentials for integrated systems are not shown in this lab guide.
2. Access the credential sheet here, ServiceNow login required: [Credentials for WDF Lab](https://servicenow.sharepoint.com/:x:/s/iaapj/IQA9-mRIzGQYSaI0ab6a--VYAQv5ZKgUGg0RVyiTdEDezq4?e=Og5Zy3).

## Integration Hub Action Endpoint

1. In [Lab Exercise: Integration Hub > Hands-on: Connection Set-up > Step 4](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/main-exercises/lab-exercise-integration-hub#hands-on-connection-setup), feel free to use other services aside from the current free tier of [beeceptor.com](https://beeceptor.com), especially if you are managing a high number of attendees (e.g. more than 10) as the free endpoint may hit access limits during your lab.
2. Updates are ongoing to make the Integration Hub endpoint used for the Action more scalable for more attendees.

## Neon Database Setup (for MCP Lab)

The [Lab Exercise: Model Context Protocol Server/Client](../extended-exercises/lab-exercise-model-context-protocol-server-client.md) requires an external cloud database hosted on [Neon](https://neon.tech) that ServiceNow connects to via MCP. This database contains a table called `VARIANCE_BASELINE_V` with 24 rows of cost center variance data used by the AI Agent during the lab.

If the existing Neon database becomes unavailable (e.g. API key expired, project deleted, free tier limits reached), follow the steps below to recreate it from scratch. No technical expertise beyond copy-pasting is required.

### Step 1: Create a Neon Account and Project

1. Go to [neon.tech](https://neon.tech) and sign up using GitHub or Google login.
2. Click **New Project**.
3. Enter a project name (e.g. `wdf-loom`).
4. Select a region close to your lab audience (e.g. **East US 2** for Americas, **Singapore** for APAC).
5. Click **Create Project**.
6. Once created, note your **Project ID** — it is shown in the project dashboard URL and looks like `shy-base-71725149`. You will need this later.

### Step 2: Create the Table and Seed Data

1. In your Neon project, navigate to **SQL Editor** from the left sidebar.
2. Open the file [neon\_setup.sql](neon_setup.sql) from this repository. Copy the **entire** contents of the file.
3. Paste it into the Neon SQL Editor and click **Run**.
4. You should see output confirming **24 rows** inserted and a sample row for cost center `CC_IT_001`:

```
 total_rows
------------
         24

 cost_center | actual_amount_usd | baseline_amount_usd | variance | variance_pct
-------------+-------------------+---------------------+----------+--------------
 CC_IT_001   |            400001 |              400000 |       -1 |            0
```

> **Tip:** The seed data is also available as a CSV file at [VARIANCE\_BASELINE\_V.csv](VARIANCE_BASELINE_V.csv) if you need to inspect or modify the data before loading.

### Step 3: Create a Neon API Key

1. In the Neon Console, click your **profile icon** (bottom-left) > **Account Settings**.
2. Go to **API Keys** > **Generate new API key**.
3. Give it a name (e.g. `wdf-lab-mcp`) and click **Create**.
4. Copy the generated key — it starts with `napi_`. **Save it securely; you will not be able to see it again.**

### Step 4: Verify the MCP Connection

Run this command in a terminal to confirm the Neon MCP server can reach your data. Replace `<YOUR_NEON_API_KEY>` and `<YOUR_PROJECT_ID>` with your values.

```bash
curl -s -X POST https://mcp.neon.tech/mcp \
  -H "Authorization: Bearer <YOUR_NEON_API_KEY>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}'
```

A successful response will contain `"serverInfo":{"name":"mcp-server-neon"}`. If you get a 401 error, double-check your API key.

### Step 5: Values to Share with Lab Participants

Provide the following to your lab participants. These are entered during [Lab Exercise: Model Context Protocol > Configure MCP Client > Step 3](../extended-exercises/lab-exercise-model-context-protocol-server-client.md#hands-on-configure-mcp-client):

| Field              | Value                        |
| ------------------ | ---------------------------- |
| **MCP Server URL** | `https://mcp.neon.tech/mcp`  |
| **API Key**        | `Bearer <YOUR_NEON_API_KEY>` |

> **Important:** The API Key field in ServiceNow must include the word **Bearer** as a prefix. For example: `Bearer napi_abc123...`. Without this prefix, the connection will fail with a 401 error.

Additionally, provide the following for [Lab Exercise: Model Context Protocol > Configure MCP Step and Tool > Step 6](../extended-exercises/lab-exercise-model-context-protocol-server-client.md#hands-on-configure-mcp-step-and-tool), to be entered in the **Tool description** field:

```
projectId: <YOUR_PROJECT_ID>
sql: SELECT cost_center, actual_amount_usd, baseline_amount_usd, variance, variance_pct FROM "VARIANCE_BASELINE_V" WHERE cost_center = '{{cost_center}}' LIMIT 1
```

> **Note:** The parameter name is `projectId` (camelCase). Using `project_id` (snake\_case) will result in an error.

### Summary of Assets

| File                                                 | Purpose                                                                                           |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [neon\_setup.sql](neon_setup.sql)                    | Complete SQL script — creates the table and inserts all 24 rows. Copy-paste into Neon SQL Editor. |
| [VARIANCE\_BASELINE\_V.csv](VARIANCE_BASELINE_V.csv) | Raw seed data in CSV format for reference or manual inspection.                                   |
