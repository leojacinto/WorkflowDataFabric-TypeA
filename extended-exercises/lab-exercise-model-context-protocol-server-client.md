---
icon: mcp
---

# Lab Exercise: Model Context Protocol Server/Client

[Take me back to main page](../)

This lab will walk you through the configuration and usage of MCP capabilities to interact with ServiceNow either as a client or as a server, allowing end users to interact with the platform as they see fit. For simplicity, this lab will cover ServiceNow acting as an MCP Client. More details on MCP Server scenarios will be added soon.

## Data flow

The data flow below shows how ServiceNow provides MCP client and server capabilities.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        ClaudeDesktop[Claude Desktop<br/>+ MCP]
    end

    subgraph "External Systems"
        CDW[(Cloud Data<br/>Warehouse)]
    end

    subgraph "ServiceNow Workflow Data Fabric and related components"
        subgraph "ServiceNow Native Tables"
            FinCase[(Finance Case<br/>Table)]
            FinVar[(Financial Variance<br/>Table)]
        end

        subgraph AI[AI & Automation]
            Agent1[Agent: Over-Budget<br/>Case Creator<br/>Zero Copy Source]
            MCPS[MCP Server]
            MCPC[MCP Client]
        end
    end

    %% MCP Server Connection
    FinVar -->|Query Data| MCPS
    FinCase -->|Query Data| MCPS
    MCPS <-->|API Communication| ClaudeDesktop

    %% MCP Client Connection
    Agent1 -->|Query Data| MCPC
    MCPC -->|Query Data| CDW

    %% User Interaction Connections
    Employee -->|Analytics| ClaudeDesktop

    %% Styling
    classDef external fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef integration fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef zeroCopy fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef native fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef ai fill:#FFB300,stroke:#F57F17,stroke-width:2px,color:#1a1a1a
    classDef user fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff

    class ERP,ExpenseAPI,SharePoint,CDW,MockERP,MockExpense,MockCDW external
    class ZeroCopySQL,ZeroCopyERP,IntHub,ExtContent integration
    class ZCCC,ZCCH,ZCCO,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,Agent3,RAG,NASK,FlowAction,MCPS,MCPC,Lens,DocIntel ai
    class Employee,EC,ClaudeDesktop user

```

## Steps

### MCP Client Preparations

1. Navigate to All > <mark style="color:green;">**a.)**</mark> type **AI Agent Studio** > <mark style="color:green;">**b.)**</mark> click on **Settings**.

<figure><img src="../.gitbook/assets/sc_mcp_agent_studio_settings_nav (3).png" alt=""><figcaption></figcaption></figure>

2. In the **Settings** page > <mark style="color:green;">**a.)**</mark> go to **Manage MCP Servers** > <mark style="color:green;">**b.)**</mark> click on **New**.

<figure><img src="../.gitbook/assets/sc_mcp_manage_servers_new.png" alt=""><figcaption></figcaption></figure>

3. Enter the details below:

<mark style="color:green;">**a.)**</mark> **Name:** **Neon MCP Lab**

<mark style="color:green;">**b.)**</mark>**&#x20;Authentication type:** **API Key**

<mark style="color:green;">**c.)**</mark> **URL:** [**https://mcp.neon.tech/mcp**](https://mcp.neon.tech/mcp)

<mark style="color:green;">**d.)**</mark>**&#x20;API Key:** Bearer \<ask\_your\_lab\_guide\_for\_key>

Note: there should be the word **Bearer** as a prefix so your value in the API Key will be something like **Bearer napi\_some\_secure\_key**

<mark style="color:green;">**e.)**</mark> **Add**

<figure><img src="../.gitbook/assets/sc_mcp_add_neon_server_details.png" alt=""><figcaption></figcaption></figure>

### Connecting to an MCP Server (Neon)

This provides the steps needed to connect ServiceNow to an MCP ([Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)) Server tool configured in Neon. ServiceNow can serve as an MCP Client to connect to any solution that has MCP support.

This exercise does not cover the creation of the MCP Service from Neon as that requires administrator rights and CDW expertise which may not be widely available to various personas.

1. Navigate to All > <mark style="color:green;">**a.)**</mark> type **AI Agent Studio** > <mark style="color:green;">**b.)**</mark> click on **Create and Manage**.

<figure><img src="../.gitbook/assets/sc_common_agent_studio_create_manage.png" alt=""><figcaption></figcaption></figure>

2. This will go to the list of workflows and agents. Go to **AI agents** tab > <mark style="color:green;">**a.)**</mark> click **search (magnifying glass)** > <mark style="color:green;">**b.)**</mark> type **Forecast Variance** and hit **Return/Enter ↵**.

<figure><img src="../.gitbook/assets/sc_zcc_agent_studio_manage.png" alt="" width="563"><figcaption></figcaption></figure>

3. Click on **Forecast Variance**.

<figure><img src="../.gitbook/assets/sc_zcc_forecast_variance_agent.png" alt=""><figcaption></figcaption></figure>

4.  Click on <mark style="color:$success;">**a.)**</mark> **more (vertical three dots)** > <mark style="color:$success;">**b.) Duplicate**</mark>

    <figure><img src="../.gitbook/assets/sc_mcp_duplicate_agent_menu.png" alt=""><figcaption></figcaption></figure>
5.  You will get a prompt to confirm whether you want to duplicate the agent. Click **Duplicate**.

    <figure><img src="../.gitbook/assets/sc_mcp_duplicate_confirm.png" alt=""><figcaption></figcaption></figure>
6.  In the new Agent screen, go to the **AI agent name** and rename it to **Forecast Variance Neon MCP Lab**.

    <figure><img src="../.gitbook/assets/sc_mcp_rename_agent_neon.png" alt=""><figcaption></figcaption></figure>
7.  In the section **Define the role and Required steps** under sub-section **List of steps**, go to step 2 after the paragraph which starts with **Get cost center obtained in...** then add **Also run the MCP tool "Get Details via Neon MCP" as a secondary check. Only return one entry (limit = 1). Columns should be \["COST\_CENTER", "ACTUAL\_AMOUNT\_USD", "BASELINE\_AMOUNT\_USD", "VARIANCE", "VARIANCE\_PCT"]**. It should look like the screenshot below.

    <figure><img src="../.gitbook/assets/sc_mcp_define_role_neon_step.png" alt=""><figcaption></figcaption></figure>
8.  Click **Save and Continue**.

    <figure><img src="../.gitbook/assets/sc_mcp_save_and_continue.png" alt=""><figcaption></figcaption></figure>
9.  Navigate to <mark style="color:green;">**a.)**</mark> **Add tools and information** > <mark style="color:green;">**b.)**</mark> **Add tool** > <mark style="color:green;">**c.)**</mark> > **MCP server tool**.

    <figure><img src="../.gitbook/assets/sc_mcp_add_tool_neon.png" alt=""><figcaption></figcaption></figure>
10. In the pop-up that appears, <mark style="color:green;">**a.)**</mark> click on the **dropdown** > <mark style="color:green;">**b.)**</mark> select **Neon MCP**.

    <figure><img src="../.gitbook/assets/sc_mcp_select_neon.png" alt=""><figcaption></figcaption></figure>
11. In the same pop-up screen, select the tool **variance-baseline-search**.

    <figure><img src="../.gitbook/assets/sc_mcp_variance_baseline_neon.png" alt=""><figcaption></figcaption></figure>
12. Still in the same pop-up screen provide the following details. Screenshot on how the settings should look like immediately follows. You only need to modify three settings and leave the rest as they are.

<mark style="color:green;">**a.)**</mark> **Name**: Get Details via Neon MCP

<mark style="color:green;">**b.)**</mark> **Tool description**:

* projectId: shy-base-71725149 (camelCase, not project\_id)
* sql: SELECT cost\_center, actual\_amount\_usd, baseline\_amount\_usd, variance, variance\_pct FROM "VARIANCE\_BASELINE\_V" WHERE cost\_center = '\{{cost\_center\}}' LIMIT 1

<mark style="color:green;">**c.)**</mark> **Execution mode**: **Autonomous**

<mark style="color:green;">**d.)**</mark>**&#x20;Save**

<figure><img src="../.gitbook/assets/sc_mcp_tool_settings_neon.png" alt="" width="563"><figcaption></figcaption></figure>

13. The pop-up will exit and you should get a section on **Model Context Protocol tools** which should look like below.

    <figure><img src="../.gitbook/assets/sc_mcp_tools_section_neon.png" alt=""><figcaption></figcaption></figure>
14. Click **Save and Continue**.

    <figure><img src="../.gitbook/assets/sc_common_save_and_continue (1).png" alt=""><figcaption></figcaption></figure>
15. Since this is copied from an existing AI Agent configuration, simply accept the default values for **Define security controls** and its 2 sub-items. Also keep A**dd triggers value** blank.

    <figure><img src="../.gitbook/assets/sc_mcp_security_defaults.png" alt=""><figcaption></figcaption></figure>
16. Finally, click on <mark style="color:green;">**a.)**</mark> **Select channels and status**. This configures the availability of the AI Agent. In this case, it is enabled and can be accessed using <mark style="color:green;">**b.)**</mark>**&#x20;Now Assist panel** toggled on as well as via <mark style="color:green;">**c.)**</mark>**&#x20;Now Assist in Virtual Agent** added as chat assistant. Click <mark style="color:green;">**d.)**</mark>**&#x20;Save and test**.

    <figure><img src="../.gitbook/assets/sc_mcp_channels_status_neon.png" alt=""><figcaption></figcaption></figure>
17. You **MIGHT** be alerted of potential duplicates but this is due to the multiple AI Agents created to test various integration scenarios. Click **Ignore and continue**.

    <figure><img src="../.gitbook/assets/sc_mcp_duplicate_warning.png" alt=""><figcaption></figcaption></figure>
18. You will be directed to the Test AI reasoning tab. To proceed with testing, <mark style="color:green;">**a.)**</mark> type **Help me process EXP-2025-IT-002-1007-01** and <mark style="color:green;">**b.)**</mark> click **Continue to Test Chat Response**.

    <figure><img src="../.gitbook/assets/sc_mcp_test_input.png" alt="" width="478"><figcaption></figcaption></figure>
19. The test will run for a few seconds and will show you that it is running the tool **Get Details in Neon MCP**. This is the additional tool you created earlier.

    <figure><img src="../.gitbook/assets/sc_mcp_test_running_neon.png" alt=""><figcaption></figcaption></figure>
20. Finally, you will notice that the **Get Details in Neon MCP** has obtained the closest matching the value of cost center CC\_IT\_001. For this exercise, we only returned the raw JSON value to demonstrate the MCP capability where we did not use any SQL or API to return the matching row; instead we just provided a high-level instruction seen in step 12.

    <figure><img src="../.gitbook/assets/sc_mcp_test_results_neon.png" alt=""><figcaption></figcaption></figure>
21. **Challenge:** once you are done with this lab, see if you can remove the tool **Extract Cost Center** and replace it completely with the data from **Get Details via Neon MCP** as seen in step 7. No hints this time. 😉

## Conclusion

Congratulations! You have created the **MCP Server** integrations that allows ServiceNow to make use of MCP capabilities from other systems outside ServiceNow, allowing LLM-powered integrations alternative APIs ,that require less development.

## Next step

You can explore a bonus use case that makes use of Stream Connect for Apache Kafka for integrations that require more throughput and data volume.

[Take me back to main page](../)
