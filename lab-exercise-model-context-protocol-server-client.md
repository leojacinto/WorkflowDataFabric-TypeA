# Lab Exercise: Model Context Protocol Server/Client

[Take me back to main page](./)

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
    classDef external fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef integration fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef zeroCopy fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef native fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef user fill:#e3f2fd,stroke:#1565c0,stroke-width:3px

    class ERP,ExpenseAPI,SharePoint,CDW,MockERP,MockExpense,MockCDW external
    class ZeroCopySQL,ZeroCopyERP,IntHub,ExtContent integration
    class ZCCC,ZCCH,ZCCO,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,Agent3,RAG,NASK,FlowAction,MCPS,MCPC,Lens,DocIntel ai
    class Employee,EC,ClaudeDesktop user

```

## Steps

### <mark style="color:red;">**Lab Admins, do this in advance!**</mark> MCP Server Preparations

1. Run the following in Snowflake for each server with the appropriate integration name. These can be done in advance as the server name prefix will be provided to you when you request for your lab environment. In this example, if you have the lab prefix lab-feb-7744 and have 10 lab participants, you will need to do steps 1 and 2 here for **https://lef-feb-7744-0001.lab.service-now.com/oauth\_redirect.do** to **https://lef-feb-7744-0010.lab.service-now.com/oauth\_redirect.do**. Take note that you have to change the title of the security name in the command as well, e.g. **SN\_MCP\_7744\_0001** to **SN\_MCP\_7744\_0010**

```sql
CREATE SECURITY INTEGRATION SN_MCP_7744_0001
  TYPE = OAUTH
  OAUTH_CLIENT = CUSTOM
  OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
  OAUTH_REDIRECT_URI = 'https://lef-feb-7744-0001.lab.service-now.com/oauth_redirect.do'
  OAUTH_ISSUE_REFRESH_TOKENS = TRUE
  OAUTH_ENFORCE_PKCE = FALSE
  ENABLED = TRUE;
```

2. Get the credentials for each users. These will need to be given to the users prior to the activity.

```sql
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('SN_MCP_7744_0001');
```

3. Once you have executed steps 1 and 2 for all your instances, you can share the link to the credentials in a file.

### MCP Client Preparations

1. Navigate to All > <mark style="color:green;">**a.)**</mark> type **AI Agent Studio** > <mark style="color:green;">**b.)**</mark> click on **Settings**.

<figure><img src=".gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

2. In the **Settings** page > <mark style="color:green;">**a.)**</mark> go to **Manage MCP Servers** > <mark style="color:green;">**b.)**</mark> click on **New**.

<figure><img src=".gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

3.  Enter the name as <mark style="color:green;">**a.)**</mark> **Snowflake MCP Lab** with <mark style="color:green;">**b.)**</mark> Authentication type OAuth 2.1 and with <mark style="color:green;">**c.)**</mark> the URL [**https://xwtgfjs-jq54573.snowflakecomputing.com/api/v2/databases/alectri/schemas/finance/mcp-servers/variance\_mcp\_server**](https://xwtgfjs-jq54573.snowflakecomputing.com/api/v2/databases/alectri/schemas/finance/mcp-servers/variance_mcp_server). Then <mark style="color:green;">**d.)**</mark> click **Next**.&#x20;

    <figure><img src=".gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
4. The following screen has more inputs required.

<mark style="color:green;">**a.)**</mark> For **Client registration type** select **Manual Registration**&#x20;

<mark style="color:green;">**b.)**</mark> For **Grant type** select **Authorization Code**&#x20;

<mark style="color:green;">**c.)**</mark> For **Token authentication method** select **Client Secret Basic**

<mark style="color:green;">**d.)**</mark> **Client ID** will be provided to you by your **Lab Admin**&#x20;

<mark style="color:green;">**e.)**</mark> **Client Secret** will be provided to you by your **Lab Admin**

<mark style="color:green;">**f.)**</mark> For **Authorization URL**, type [**https://xwtgfjs-jq54573.snowflakecomputing.com/oauth/authorize**](https://xwtgfjs-jq54573.snowflakecomputing.com/oauth/authorize)

<mark style="color:green;">**g.)**</mark> For **Token URL**, type [**https://xwtgfjs-jq54573.snowflakecomputing.com/oauth/token-request**](https://xwtgfjs-jq54573.snowflakecomputing.com/oauth/token-request)&#x20;

<mark style="color:green;">**h.)**</mark> Click **Add**

<figure><img src=".gitbook/assets/image (40).png" alt="" width="563"><figcaption></figcaption></figure>

5.  Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Connection & Credential Aliases** then <mark style="color:green;">**b.)**</mark> click **Connections & Credentials > Connection & Credential Aliases**.

    <figure><img src=".gitbook/assets/image (63).png" alt=""><figcaption></figcaption></figure>
6. Search for an entry with the prefix **AutoGen-Snowflake MCP Lab**. Take not of the Lab! There might be an entry with a similar prefix.

<figure><img src=".gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

7. You can configure the alias by going through the link under the <mark style="color:green;">**a.)**</mark>**&#x20;Name** field or <mark style="color:green;">**b.)**</mark> Credential field. The succeeding screens are through the **Credential** field so click <mark style="color:green;">**b.)**</mark>.

<figure><img src=".gitbook/assets/image (45).png" alt=""><figcaption></figcaption></figure>

8. Ctrl  / ⌘ + click on the **i-icon** in the screen that follows to open a new window. <mark style="color:green;">**You will need to come back to this window later!**</mark>

<figure><img src=".gitbook/assets/image (46).png" alt=""><figcaption></figcaption></figure>

9.  In the screen that follows, click on a line below **OAuth Entity Scope** which is under the section **OAuth Entity Profile Scopes**. A small dialog box will pop-up. Click on the **magnifying class icon**.

    <figure><img src=".gitbook/assets/image (87).png" alt=""><figcaption></figcaption></figure>
10. In the next dialog box that appears, click **New**.

<figure><img src=".gitbook/assets/image (48).png" alt=""><figcaption></figcaption></figure>

11. Beside <mark style="color:green;">**a.)**</mark> Name and <mark style="color:green;">**b.)**</mark> OAuth scope, type **session:role:MCP\_SERVICE\_ROLE**.

<figure><img src=".gitbook/assets/image (50).png" alt=""><figcaption></figcaption></figure>

12. Beside OAuth provider, <mark style="color:green;">**a.)**</mark> type AutoGen and <mark style="color:green;">**b.)**</mark> select the entry with the prefix **AutoGen-Snowflake MCP Lab**, then <mark style="color:green;">**c.)**</mark> click **Submit**.

<figure><img src=".gitbook/assets/image (54).png" alt=""><figcaption></figcaption></figure>

13. This will lead you back to the small dialog box, click the **check mark** to confirm your settings.

<figure><img src=".gitbook/assets/image (51).png" alt=""><figcaption></figcaption></figure>

14. This will lead to the screen below.

<figure><img src=".gitbook/assets/image (53).png" alt=""><figcaption></figcaption></figure>

15. Do the same steps you have done for **sesion:role:MCP\_SERVICE\_ROLE** but this time for the value **refresh\_token**. Put the value **refresh\_token** for **Name** and **OAuth scope**.

<figure><img src=".gitbook/assets/image (52).png" alt=""><figcaption></figcaption></figure>

16. For OAuth provider, simply get your **Recent selections** item which has the **AutoGen-Snowflake MCP Lab** prefix.

<figure><img src=".gitbook/assets/image (55).png" alt=""><figcaption></figcaption></figure>

17. You will see the **sesion:role:MCP\_SERVICE\_ROLE** and **refresh\_token** entries stored. Right click on the header and click **Save**.

<figure><img src=".gitbook/assets/image (59).png" alt=""><figcaption></figcaption></figure>

19. Go back to your tab which has the **OAuth 2.0 Credentials** open and click **Get OAuth Token**.

<figure><img src=".gitbook/assets/image (58).png" alt=""><figcaption></figcaption></figure>

20. Your Lab Admin will provide the <mark style="color:green;">**a.)**</mark>**&#x20;Username** and <mark style="color:green;">**b.)**</mark>**&#x20;Password** and once entered  <mark style="color:green;">**c.)**</mark> click **Sign in**.

<figure><img src=".gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>

21. Click **Allow**.

<figure><img src=".gitbook/assets/image (61).png" alt=""><figcaption></figcaption></figure>

22. Your will have a refreshed OAuth token that will last for 1 hour before it expires. You can now connect to the Snowflake cloud data warehouse via MCP and call MCP tools using ServiceNow's AI Agents.

<figure><img src=".gitbook/assets/image (62).png" alt=""><figcaption></figcaption></figure>

### Connecting to an MCP Server (Snowflake)

This provides the steps needed to connect ServiceNow to an MCP ([Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)) Server tool configured in Snowflake. ServiceNow can serve as an MCP Client to connect to any solution that has MCP support.

This exercise does not cover the creation of the MCP Service from Snowflake as that requires administrator rights and CDW expertise which may not be widely available to various personas.

1. Navigate to All > <mark style="color:green;">**a.)**</mark> type **AI Agent Studio** > <mark style="color:green;">**b.)**</mark> click on **Create and Manage**.

<figure><img src=".gitbook/assets/image (69).png" alt=""><figcaption></figcaption></figure>

2. This will go to the list of workflows and agents. Go to **AI agents** tab > <mark style="color:green;">**a.)**</mark> click **search (magnifying glass)** > <mark style="color:green;">**b.)**</mark> type **Forecast Variance** and hit **Return/Enter ↵**.

<figure><img src=".gitbook/assets/sc_zcc_agent_studio_manage.png" alt="" width="563"><figcaption></figcaption></figure>

3. Click on **Forecast Variance**.

<figure><img src=".gitbook/assets/sc_zcc_forecast_variance_agent.png" alt=""><figcaption></figcaption></figure>

4.  Click on <mark style="color:$success;">**a.)**</mark> **more (vertical three dots)** > <mark style="color:$success;">**b.) Duplicate**</mark>

    <figure><img src=".gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>
5.  You will get a prompt to confirm whether you want to duplicate the agent. Click **Duplicate**.

    <figure><img src=".gitbook/assets/image (20).png" alt=""><figcaption></figcaption></figure>
6.  In the new Agent screen, go to the **AI agent name** and rename it to **Forecast Variance Snowflake MCP Lab**.

    <figure><img src=".gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>
7.  In the section **Define the role and Required steps** under sub-section **List of steps**, go to step 2 after the paragraph which starts with **Get cost center obtained in...** then add **Also run the MCP tool "Get Details via Snowflake MCP" as a secondary check. Only return one entry (limit = 1). Columns should be \["COST\_CENTER", "ACTUAL\_AMOUNT\_USD", "BASELINE\_AMOUNT\_USD", "VARIANCE", "VARIANCE\_PCT"]**. It should look like the screenshot below.

    <figure><img src=".gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>
8.  Click **Save and Continue**.

    <figure><img src=".gitbook/assets/image (49).png" alt=""><figcaption></figcaption></figure>
9.  Navigate to <mark style="color:green;">**a.)**</mark> **Add tools and information** > <mark style="color:green;">**b.)**</mark> **Add tool** > <mark style="color:green;">**c.)**</mark> > **MCP server tool**.

    <figure><img src=".gitbook/assets/image (56).png" alt=""><figcaption></figcaption></figure>
10. In the pop-up that appears, <mark style="color:green;">**a.)**</mark> click on the **dropdown** > <mark style="color:green;">**b.)**</mark> select **Snowflake MCP**.

    <figure><img src=".gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>
11. In the same pop-up screen, select the tool **variance-baseline-search**.

    <figure><img src=".gitbook/assets/image (74).png" alt="" width="375"><figcaption></figcaption></figure>
12. Still in the same pop-up screen provide the following details. Screenshot on how the settings should look like immediately follows. You only need to modify three settings and leave the rest as they are.

<mark style="color:green;">**a.)**</mark> **Name**: **Get Details in Snowflake MCP**

<mark style="color:green;">**b.)**</mark> **Tool description**:&#x20;

* query: Get the details via Snowflake MCP using the cost center taken from "Extract Cost Center" step (e.g. "CC\_IT\_001")
* columns: \["COST\_CENTER", "ACTUAL\_AMOUNT\_USD", "BASELINE\_AMOUNT\_USD", "VARIANCE", "VARIANCE\_PCT"]
* limit: 1

<mark style="color:green;">**c.)**</mark> **Execution mode**: **Autonomous**

<mark style="color:green;">**d.)**</mark>**&#x20;Save**

<figure><img src=".gitbook/assets/image (82).png" alt="" width="563"><figcaption></figcaption></figure>

13. The pop-up will exit and you should get a section on **Model Context Protocol tools** which should look like below.

    <figure><img src=".gitbook/assets/image (83).png" alt=""><figcaption></figcaption></figure>
14. Click **Save and Continue**.

    <figure><img src=".gitbook/assets/image (77).png" alt=""><figcaption></figcaption></figure>
15. Since this is copied from an existing AI Agent configuration, simply accept the default values for **Define security controls** and its 2 sub-items. Also keep A**dd triggers value** blank.

    <figure><img src=".gitbook/assets/image (78).png" alt=""><figcaption></figcaption></figure>
16. Finally, click on <mark style="color:green;">**a.)**</mark> **Select channels and status**. This configures the availability of the AI Agent. In this case, it is enabled and can be accessed using <mark style="color:green;">**b.)**</mark>**&#x20;Now Assist panel** toggled on as well as via <mark style="color:green;">**c.)**</mark>**&#x20;Now Assist in Virtual Agent** added as chat assistant. Click <mark style="color:green;">**d.)**</mark>**&#x20;Save and test**.

    <figure><img src=".gitbook/assets/image (79).png" alt=""><figcaption></figcaption></figure>
17. You **MIGHT**  be alerted of potential duplicates but this is due to the multiple AI Agents created to test various integration scenarios. Click **Ignore and continue**.

    <figure><img src=".gitbook/assets/image (80).png" alt=""><figcaption></figcaption></figure>
18. You will be directed to the Test AI reasoning tab. To proceed with testing, <mark style="color:green;">**a.)**</mark> type **Help me process EXP-2025-IT-002-1007-01** and <mark style="color:green;">**b.)**</mark> click **Continue to Test Chat Response**.

    <figure><img src=".gitbook/assets/image (81).png" alt="" width="478"><figcaption></figcaption></figure>
19. The test will run for a few seconds and will show you that it is running the tool **Get Details in Snowflake MCP**. This is the additional tool you created earlier.

    <figure><img src=".gitbook/assets/image (85).png" alt=""><figcaption></figcaption></figure>
20. Finally, you will notice that the **Get Details in Snowflake MCP** has obtained the closest matching the value of cost center CC\_IT\_001. For this exercise, we only returned the raw JSON value to demonstrate the MCP capability where we did not use any SQL or API to return the matching row; instead we just provided a high-level instruction seen in step 12.

    <figure><img src=".gitbook/assets/image (86).png" alt=""><figcaption></figcaption></figure>
21. **Challenge:** once you are done with this lab, see if you can remove the tool **Extract Cost Center** and replace it completely with the data from **Get Details via Snowflake MCP** as seen in step 7. No hints this time. 😉

## Troubleshooting

1. If the Now Assist Agent is not showing the action being executed and the history of chats like below, wait for 5 minutes or so and refresh your browser. This is primarily due to the instance's fresh Now Assist settings which you have just configured earlier.

<figure><img src=".gitbook/assets/image (2) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

2. If you get messages in Now Assist from the agent saying messages like below, this just means that indexing of the tables needed by the agent to search transactions is not yet completed. Wait for 10 to 15 minutes.

* There is no available information indicating similar transactions for this vendor in the past based on the cost center being processed.
*   Based on the available information, there is insufficient data to determine whether the results are mostly 'On Target', 'Over Budget', or 'Under Budget.' Please provide additional details or context for a more accurate evaluation. **Do the following steps to force an indexing job, but this is not a guaranteed fix if there is a high load in the shared lab ML services used in AI search**.

    * Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Indexed Sources** > <mark style="color:green;">**b.)**</mark> click **AI Search > AI Search Index >** and Ctrl  / ⌘ + click **Indexed Sources** to open a new window.

    <figure><img src=".gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

    *   Search for **Sources** with the string <mark style="color:green;">**a.)**</mark> \*x\_snc\_forecast then Ctrl  / ⌘ + click both <mark style="color:green;">**b.)**</mark> **Cost Center Budget History Indexed Source** and <mark style="color:green;">**c.)**</mark>**&#x20;Expense Transactions Indexed Source** so you have two new windows for these objects.&#x20;

        <figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>
    * In the new window for **Center Budget History Indexed Source**, click **Index All Tables**.

    <figure><img src=".gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

    *   In the new window for **Expense Transactions Indexed Source**, click **Index All Tables**.

        <figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>
    * Once done, you can re-execute your agent.

## Conclusion

Congratulations! You have created the **MCP Server** integrations that allows ServiceNow to make use of MCP capabilities from other systems outside ServiceNow, allowing LLM-powered integrations alternative APIs ,that require less development.

## Next step

You can explore a bonus use case that makes use of Stream Connect for Apache Kafka for integrations that require more throughput and data volume.

[Take me back to main page](./)
