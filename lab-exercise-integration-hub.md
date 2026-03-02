# Lab Exercise: Integration Hub

[Take me back to main page](./)

This lab will walk you through the configuration and usage of **Actions** and **Flows** to get expense data from an external source periodically or ad hoc and trigger an agent which will evaluate the expense data and create a Finance case if the involved cost center will be over budget.

There are dedicated Integration Hub and Flow Designer labs; hence, the focus of this exercise is to walk through the configurations in AI Agent Studio and Flow Designer. There is an exercise at the end for you to configure an **Action**, which aims provide an understanding on how the AI Agents are triggered.

## Data flow

The data flow below shows how ServiceNow will consume REST API endpoints via Integration Hub Spokes then further processed by a Flow so the entries will be written in the scoped table.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/> Workspace with Now Assist]
    end

    subgraph "External Systems"
        ExpenseAPI[Expense Event<br/>API]
    end

    subgraph "ServiceNow Workflow Data Fabric and related components"
        subgraph "Data Integration Layer"
            IntHub[Integration Hub<br/>Spoke/Flow]
        end

        subgraph "Zero Copy Tables - Read Only"
            ZCCC[(Cost Centre)]
        end

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
            FinCase[(Finance Case<br/>Table)]
        end

        subgraph "AI & Automation"
            Agent2[Agent: Proactive<br/>Budget Alert<br/>Integration Hub Source]
            RAG[RAG - Retrieval<br/>Augmented Generation]
            FlowAction[Flow Action]
        end
    end

    %% Data Flow Connections
    ExpenseAPI -->|Real-time Events| IntHub
    IntHub -->|Write| ExpenseTable

    %% Agent 2 Workflow - Integration Hub Source
    ExpenseTable -->|Incoming Event| Agent2
    ZCCC -->|Current Budget| Agent2
    Agent2 -->|Create Case| FinCase
    Agent2 <-->|Trend Analysis| RAG
    Agent2 <-->|Flows/Subflows/Actions| FlowAction

    %% User Interaction Connections
    Employee -->|Ask Questions<br/>View/Update Cases| EC
    EC -->|Search & Query| FinCase

    %% Styling
    classDef external fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef integration fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef zeroCopy fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef native fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef user fill:#e3f2fd,stroke:#1565c0,stroke-width:3px

    class ExpenseAPI,SharePoint external
    class IntHub,ExtContent integration
    class ZCCC zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent2,NLQuery,RAG,NASK,FlowAction ai
    class MockExpense external
    class Employee,EC user
```

## Steps

### Platform Configuration

1. Back as **admin** user, this preparation section includes setting up of the scope, authorisation and Now Assist configurations. You can skip this if you have done it for [Lab Exercise: Zero Copy Connectors](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/3_zero_copy).
2.  Ensure you are in the correct scope. Click on the <mark style="color:green;">**a.)**</mark> **scope** (globe icon) and <mark style="color:green;">**b.)**</mark> **Forecast Variance**, this time <mark style="color:red;">**WITHOUT**</mark> your initials.

    <figure><img src=".gitbook/assets/sc_fund_exercise_scope.png" alt=""><figcaption></figcaption></figure>
3.  Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **AI Agent Studio** > <mark style="color:green;">**b.)**</mark> click on **Users**.

    <figure><img src=".gitbook/assets/sc_common_agent_studio_users_nav.png" alt=""><figcaption></figcaption></figure>
4.  Search for <mark style="color:green;">**a.)**</mark> **System Administrator** then hit **Return/Enter ↵** > <mark style="color:green;">**b.)**</mark> click on **admin**.

    <figure><img src=".gitbook/assets/sc_common_search_admin_user.png" alt=""><figcaption></figcaption></figure>
5.  In the **Roles** tab, click **Edit**.

    <figure><img src=".gitbook/assets/sc_common_roles_tab_edit.png" alt=""><figcaption></figcaption></figure>
6.  Search for <mark style="color:green;">**a.)**</mark> **sn\_aia.admin** > <mark style="color:green;">**b.)**</mark> click on **sn\_aia.admin** > <mark style="color:green;">**c.)**</mark> click on **>** to move the role to the right panel > then <mark style="color:green;">**b.)**</mark> click **Save**. You will notice that there are also roles for integration and viewer purposes which can be assigned for users who will need less privileges.

    <figure><img src=".gitbook/assets/sc_ihub_roles_sn_aia_save.png" alt=""><figcaption></figcaption></figure>
7.  You will get <mark style="color:green;">**a.)**</mark> messages such as **Adding Role agent\_role\_config\_viewer to admin**, there will be 4 of such messages > <mark style="color:green;">**b.)**</mark> right-click on the top panel and click **Save**.

    <figure><img src=".gitbook/assets/sc_ihub_role_messages_save.png" alt=""><figcaption></figcaption></figure>
8.  <mark style="color:red;">**IMPORTANT**</mark>. Log out and log back in.

    <figure><img src=".gitbook/assets/sc_common_logout.png" alt="" width="254"><figcaption></figcaption></figure>
9.  Once logged back in navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Assistant Designer** then <mark style="color:green;">**b.)**</mark> click **Conversational Interfaces > Assistant Designer**. This will open a new tab.

    <figure><img src=".gitbook/assets/sc_common_assistant_designer_nav.png" alt="" width="337"><figcaption></figcaption></figure>
10. Go to **Now Assist Panel - Platform (default)** > **Edit**.

    <figure><img src=".gitbook/assets/sc_common_now_assist_panel_edit.png" alt="" width="375"><figcaption></figcaption></figure>
11. Under **Continue customizing this assistant** > **Add display experiences** > click **Go to display experiences**.

    <figure><img src=".gitbook/assets/sc_common_display_experiences_link.png" alt="" width="563"><figcaption></figcaption></figure>
12. Under **Settings** > <mark style="color:green;">**a.)**</mark>**&#x20;Display experiences**, make sure that <mark style="color:green;">**b.)**</mark>**&#x20;Unified Navigation app shell** is selected. If it is not added, you may need to select it from **Add ServiceNow platform** dropdown menu. Click <mark style="color:green;">**c.)**</mark> **Save** then <mark style="color:green;">**d.)**</mark>**&#x20;Activate**. This step is needed to ensure that the Now Assist panel is accessible when AI Agents are triggered.

    <figure><img src=".gitbook/assets/sc_common_unified_nav_settings.png" alt=""><figcaption></figcaption></figure>
13. Click on the **Assistant Designer** logo at the top left. You may need to refresh your page to make sure it has picked up the latest status of **Now Assist Panel - Platform (default)**.

    <figure><img src=".gitbook/assets/sc_common_assistant_designer_logo.png" alt="" width="240"><figcaption></figcaption></figure>
14. Go to **Now Assist in Virtual Agent (default)** > **Edit**. Note that this is another configuration tile!

    <figure><img src=".gitbook/assets/image (1).png" alt="" width="375"><figcaption></figcaption></figure>
15. Under **Continue customizing this assistant** > **Add display experiences** > click **Go to display experiences**.

    <figure><img src=".gitbook/assets/sc_common_display_experiences_link.png" alt="" width="563"><figcaption></figcaption></figure>
16. Under **Settings** > <mark style="color:green;">**a.)**</mark>**&#x20;Display experiences**, make sure that <mark style="color:green;">**b.)**</mark>**&#x20;Employee Center** is selected. If it is not added, you may need to select it from **Add portal** dropdown menu. Click <mark style="color:green;">**c.)**</mark> **Save** then <mark style="color:green;">**d.)**</mark>**&#x20;Activate**. This step is needed to ensure that the Virtual Agent is accessible in Employee Center where most end users will do their day to day tasks such as processing and opening cases.

<figure><img src=".gitbook/assets/sc_common_employee_center_display.png" alt=""><figcaption></figcaption></figure>

17. Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Now Assist Admin** then <mark style="color:green;">**b.)**</mark> click **Now Assist Admin > Experiences**.

<figure><img src=".gitbook/assets/sc_common_now_assist_admin_nav.png" alt="" width="298"><figcaption></figcaption></figure>

18. Go to> <mark style="color:green;">**a.)**</mark> **Now Assist panel** then <mark style="color:green;">**b.)**</mark> click **Turn on**. This is an aditional configuration to ensure **Now Assist panel** is accessible.

<figure><img src=".gitbook/assets/sc_common_now_assist_turn_on.png" alt="" width="563"><figcaption></figcaption></figure>

### Action configuration

The scoped **Action** is a key feature for the trigger that obtains expense data via REST API. If you wish to learn more on how Flows and AI Agents can get high more granular and higher throughput of data through streaming, have a look at the bonus exercise on [Stream Connect for Apache Kafka](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/99_kafka_stream_connect).

1.  Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Connection & Credential Aliases** then <mark style="color:green;">**b.)**</mark> click **Connections & Credentials > Connection & Credential Aliases**.

    <figure><img src=".gitbook/assets/sc_common_conn_cred_aliases_nav.png" alt=""><figcaption></figcaption></figure>
2.  Search for <mark style="color:green;">**a.)**</mark>**&#x20;Get Expense Even**t then <mark style="color:green;">**b.)**</mark> click on **Get Expense Event**. This is a pre-configured alias to reduce the rewiring needed for this lab exercise.

    <figure><img src=".gitbook/assets/sc_ihub_search_get_expense_event.png" alt=""><figcaption></figcaption></figure>
3.  In the next screen, navigate to **Connections** > **New**. In this alias, we are creating a new connection which will get data from the REST API endpoint and serve as trigger for our AI Agent.

    <figure><img src=".gitbook/assets/sc_ihub_connections_new.png" alt=""><figcaption></figcaption></figure>
4.  Provide <mark style="color:green;">**a.)**</mark> **Name** as **Get Expense Event**, <mark style="color:green;">**b.)**</mark>**&#x20;Connection URL** as [**https://expense-event.free.beeceptor.com**](https://expense-event.free.beeceptor.com) then <mark style="color:green;">**c.)**</mark> click **Submit**. The structure of the table in [Lab Exercise: Fundamentals](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-fundamentals) is based on the data coming from this REST API endpoint. The data from this endpoint will be written into the scoped table through a scoped **Action**.

    <figure><img src=".gitbook/assets/sc_ihub_connection_url_submit.png" alt=""><figcaption></figcaption></figure>
5.  Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **ServiceNow Studio** then <mark style="color:green;">**b.)**</mark> click **App Engine > ServiceNow Studio**. This will open a new tab.

    <figure><img src=".gitbook/assets/sc_ihub_servicenow_studio_nav.png" alt=""><figcaption></figcaption></figure>
6. In the **ServiceNow Studio** tab that pops up under **Apps**, <mark style="color:green;">**a.)**</mark> type Forecast Variance and <mark style="color:green;">**b.)**</mark> click on **Forecast Variance**. Note that you may need to search for a different a App name if you used a different label for your scope.

<figure><img src=".gitbook/assets/sc_ihub_studio_forecast_variance.png" alt="" width="334"><figcaption></figcaption></figure>

3. In this current version of the lab, we will  walk you through the components. <mark style="color:green;">**a.)**</mark> **Go to Automation** > **Actions** > **Get Expense Event**. It will open the Action and from there <mark style="color:green;">**b.)**</mark> **click on Get Expense Event**. The <mark style="color:green;">**c.)**</mark> **Base URL** here is coming from a service that creates the expense event and the <mark style="color:green;">**d.)**</mark> **Imported Specifications** are also generated from the same service. No further action is needed in this section.

<figure><img src=".gitbook/assets/sc_ihub_studio_action_1.png" alt=""><figcaption></figcaption></figure>

4. Got to <mark style="color:green;">**a.)**</mark> Outputs where <mark style="color:green;">**b.)**</mark> output is generated based on the Imported Specifications. This makes the table structure in [Lab Exercise: Fundamentals](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-fundamentals) critical as missing or mismatched fields will cause this **Action** to fail in getting data from the REST endpoint.

<figure><img src=".gitbook/assets/sc_ihub_studio_action_2.png" alt=""><figcaption></figcaption></figure>

5. You now have familiarity of the **Action** used by the **Subflow** needed to trigger the **AI agent**, which is described in the next section.

### Custom Forecast Variance AI agent

This is a walk through of how an AI agent with equipped with both deterministic and probabilistic capabilities can automate research and validation of cost center history and expenses; as well as creation of Finance Cases should cost centers be above their budget allocations. <mark style="color:red;">**Note:**</mark> this is a custom AI agent pre-configured in the lab instance provided in ServiceNow-led lab sessions; this is not an OOTB agent.

1.  Go to **All** > type **x\_snc\_forecast\_v\_0\_expense\_transaction\_event.list** and hit **Return/Enter ↵**. Ensure that it is empty.

    <figure><img src=".gitbook/assets/sc_common_expense_event_nav.png" alt=""><figcaption></figcaption></figure>
2. This list **SHOULD** be **EMPTY** for the AI agent to work. If it is **NOT** empty, <mark style="color:green;">**a.)**</mark> click on all the items by clicking the **top-rightmost check box** > <mark style="color:green;">**b.)**</mark> click **Action on selected rows...** > <mark style="color:green;">**c.)**</mark> click **Delete** > <mark style="color:green;">**d.)**</mark> click **Delete** again. The flow does not have robust exception handling for this lab so this manual step is required to ensure that the scripts will run properly.

<figure><img src=".gitbook/assets/sc_ihub_expense_event_delete.png" alt=""><figcaption></figcaption></figure>

3.  Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **AI Agent Studio** > <mark style="color:green;">**b.)**</mark> click on **Create and Manage**.

    <figure><img src=".gitbook/assets/sc_common_agent_studio_create_manage.png" alt=""><figcaption></figcaption></figure>
4. This will go to the list of Agentic workflows and AI agents. Go to **AI agents** tab > <mark style="color:green;">**a.)**</mark> click **search (magnifying glass)** > <mark style="color:green;">**b.)**</mark> type **Forecast Variance** **Integration Hub Trigger** and hit **Return/Enter ↵**.

<figure><img src=".gitbook/assets/sc_ihub_agent_studio_manage.png" alt="" width="563"><figcaption></figcaption></figure>

5. Click on **Forecast Variance Integration Hub Trigger** to make adjustments to the pre-configured AI Agent.

<figure><img src=".gitbook/assets/sc_ihub_forecast_variance_agent.png" alt="" width="563"><figcaption></figcaption></figure>

6.  Click on **Define the specialty**. This shows all the instructions for this AI Agent created in plain English. The **List of steps** describes the sequence, purpose, and nuances of the tools configured, which are shown in the next section. No further action is required in this section.

    <figure><img src=".gitbook/assets/sc_ihub_define_specialty.png" alt=""><figcaption></figcaption></figure>
7.  Next, click on **Add tools and information**. This is a collection of **Search retrievals** and **Subflows** that are used by the agent. The purpose and sequence of these tools are also described in the section **Define the specialty**. No further action is required in this section but feel free to explore the configurations of each of the tools.

    <figure><img src=".gitbook/assets/sc_ihub_add_tools_info.png" alt=""><figcaption></figcaption></figure>
8.  Under **Define security controls** > <mark style="color:green;">**a.)**</mark> click **Define data access** > <mark style="color:green;">**b.)**</mark> select **Dynamic user** from the drop down then > <mark style="color:green;">**c.)**</mark> add **admin** user as the **Approved role** if the field is not filled out yet. For this exercise we are using permissive authorisations but this is where you can tighten authorisations for your agents allowing mechanisms such as inheriting the authorisations of logged in user (Dynamic identity type) or a predefined set of access (AI User identity type).

    <figure><img src=".gitbook/assets/sc_ihub_define_security.png" alt=""><figcaption></figcaption></figure>
9.  Next, click on **Define trigger**, which is a key part of this exercise.&#x20;

    <figure><img src=".gitbook/assets/sc_ihub_define_trigger_view.png" alt=""><figcaption></figcaption></figure>
10. <mark style="color:red;">**\[IMPORTANT STEP]**</mark> Due to a bug related to the update set for this lab, if there is an existing trigger, you will need to delete that and **re-create**. Click the <mark style="color:green;">**a.)**</mark> **delete** icon then <mark style="color:green;">**b.)**</mark> click **Add trigger**.

    <figure><img src=".gitbook/assets/sc_ihub_trigger_delete_add.png" alt=""><figcaption></figcaption></figure>
11. Enter the details below for the trigger. These are basic information to identify your trigger. When the parameters in the trigger are satisfied, this will fire off the AI agent.

<mark style="color:green;">**a.)**</mark> **Select trigger**: **Created**

<mark style="color:green;">**b.)**</mark> **Name**: **Create New Expense Transaction Event \<YOUR INITIALS>**

<mark style="color:green;">**c.)**</mark> **Trigger**: toggle **ON**

<mark style="color:green;">**d.)**</mark> Scroll down

<figure><img src=".gitbook/assets/sc_ihub_trigger_details_1.png" alt=""><figcaption></figcaption></figure>

12. More details to add below before finally saving the trigger configuration. These configurations include the target table and field and condition that needs to be satisfied to fire off the trigger, as well as logging.&#x20;

<mark style="color:green;">**a.)**</mark> **Table**: **Expense Transaction Event**

<mark style="color:green;">**b.)**</mark> **Field**: **Vendor**

<mark style="color:green;">**c.)**</mark> **Condition** > **Operator**: **is not empty**

<mark style="color:green;">**d.)**</mark> **Sys\_user**: **Owner**

<mark style="color:green;">**e.)**</mark> **Save**

<figure><img src=".gitbook/assets/sc_ihub_trigger_details_2.png" alt=""><figcaption></figcaption></figure>

13. Click **Save and Continue**.

<figure><img src=".gitbook/assets/sc_common_save_and_continue (1).png" alt=""><figcaption></figcaption></figure>

14. Finally, click on <mark style="color:green;">**a.)**</mark> **Select channels and status**. This configures the availability of the AI agent. In this case, it is enabled and can be accessed using <mark style="color:green;">**b.)**</mark>**&#x20;Now Assist panel** toggled on as well as via <mark style="color:green;">**c.)**</mark>**&#x20;Now Assist in Virtual Agent** added as chat assistant. Make sure your configuration is set as below. Once done, <mark style="color:green;">**d.)**</mark> click **Save**. <mark style="color:green;">**Keep this browser window open! You will need again it later**</mark>.

<figure><img src=".gitbook/assets/sc_ihub_select_channels.png" alt=""><figcaption></figcaption></figure>

### Runtime of Flow, Actions, and AI agents

1.  In a **new browser window**, go to All > <mark style="color:green;">**a.)**</mark> type **Flow Designer** and go to <mark style="color:green;">**b.)**</mark> **Process Automation** > **Flow Designer**. This will open the app in a new tab.

    <figure><img src=".gitbook/assets/sc_ihub_flow_designer_nav.png" alt=""><figcaption></figcaption></figure>
2. In the new **Flow Designer** tab that just opened, <mark style="color:green;">**a.)**</mark> click **Subflows** > <mark style="color:green;">**b.)**</mark> **more (vertical three dots)** > <mark style="color:green;">**c.)**</mark> type Get Expense Event then <mark style="color:green;">**d.)**</mark> click **Apply**.&#x20;

<figure><img src=".gitbook/assets/sc_ihub_flow_search.png" alt="" width="563"><figcaption></figcaption></figure>

3. This will lead to the subflow below. We will not cover the build of this **Flow** in detail in this lab exercise. The key thing to note is that it makes use of the **Action** also called **Get Expense Event** to update the **Transaction Event Record** table which is critical for the automation.

<figure><img src=".gitbook/assets/sc_ihub_get_expense_event.png" alt="" width="563"><figcaption></figcaption></figure>

4. On the top right corner of the same **Subflow** screen, click **Test**. This will run an actual execution of the **Get Expense Event** subflow and get the data from the REST API endpoint we created earlier.

<figure><img src=".gitbook/assets/sc_ihub_test_flow.png" alt="" width="355"><figcaption></figcaption></figure>

5. A pop-up will appear. Click **Run Test**.

<figure><img src=".gitbook/assets/sc_ihub_test_run.png" alt="" width="563"><figcaption></figcaption></figure>

6. After a few seconds, a link which states **Your test has finished running. View the subflow execution details.** - click on it.

<figure><img src=".gitbook/assets/sc_ihub_test_link.png" alt="" width="563"><figcaption></figcaption></figure>

7. If everything is working as expected, all the steps would be either <mark style="color:green;">**Completed**</mark> or <mark style="color:green;">**Evaluated - True**</mark>.

<figure><img src=".gitbook/assets/sc_ihub_test_results.png" alt=""><figcaption></figcaption></figure>

8.  Go back to the earlier browser window with **AI Agent Studio**. You will notice that there is a new **Now Assist badge**. This is the AI agent at work in the back end because the **Get Expense Event** subflow has triggered a change in the **Expense Transaction Event** table. Click on the **Now Assist icon** with the updated badge count. If the **Now Assist badge** does not appear, simply reload your page.

    <figure><img src=".gitbook/assets/sc_ihub_now_assist_badge_notification.png" alt=""><figcaption></figcaption></figure>
9.  This will open the **Now Assist** chat. Click on the two-headed diagonal arrow to Enter **Modal**.

    <figure><img src=".gitbook/assets/sc_ihub_now_assist_chat_expand.png" alt=""><figcaption></figcaption></figure>
10. Here is an overview of the steps that were executed.

<mark style="color:green;">**a.)**</mark> Expand **Planning the next steps** show tools used.

<mark style="color:green;">**b.)**</mark> Note the **event ID** extracted from the expense event.

<mark style="color:green;">**c.)**</mark> Note the **cost\_center** and **vendor** extracted from the expense event.

<mark style="color:green;">**d.)**</mark> The clickable results from the **Retrieval-augmented Generation (RAG) search** are shown. This step helps you check relevant entries for the cost center associated with the expense event so you can do further investigation if needed.

<mark style="color:green;">**e.)**</mark> You can also access the **RAG search** results for the vendors associated with the expense event.

<mark style="color:green;">**f.)**</mark> Finally, if the expense event will lead to the associated cost center being over budget, the total cost center expense and the **Finance Case** created for exceeding the budget for further review and action is listed. In this case it is FINC0010020.

<figure><img src=".gitbook/assets/sc_ihub_agent_results_overview.png" alt=""><figcaption></figcaption></figure>

12. Navigate to Workspaces > <mark style="color:green;">**a.)**</mark> type **Finance Operations Workspace** and click on the <mark style="color:green;">**b.)**</mark> workspace with the same name. We will now check if Finance Case has been created successfully.

    <figure><img src=".gitbook/assets/sc_common_fow_nav.png" alt=""><figcaption></figcaption></figure>
13. For this exercise, we are not impersonating a persona so you remain as the System user.

    <figure><img src=".gitbook/assets/sc_common_fow_system_user.png" alt=""><figcaption></figcaption></figure>
14. Go to <mark style="color:green;">**a.)**</mark> **list (list icon)** > <mark style="color:green;">**b.)**</mark> **Lists** > <mark style="color:green;">**c.)**</mark> sort by **Number** descending/ascending > <mark style="color:green;">**d.)**</mark> or look for the Finance case created by the AI agent, FINC0010020 in the example above.

<figure><img src=".gitbook/assets/sc_ihub_finance_case_list.png" alt=""><figcaption></figcaption></figure>

## Troubleshooting

1. If the URL in **Action Configuration** > step 4 is failed to fetch data due to rate limiting or any other reason, you can upload the file here to trigger a created/updated row in x\_snc\_forecast\_v\_0\_expense\_transaction\_event. [Get the XML file here](https://raw.githubusercontent.com/leojacinto/WorkflowDataFabric-TypeA/refs/heads/main/.gitbook/assets/x_snc_forecast_v_0_expense_transaction_event.xml). Additional notes:

* If you are not using the action to fetch data via API and are uploading the XML file, change the trigger in **Custom Forecast Variance AI Agent** > step 11 to **Created or updated**, instead of **Created**.
*   This approach is not representative of real integration scenario as you are only doing a file upload. A **Created** trigger will not initiate from an upload.

    <figure><img src=".gitbook/assets/sc_ihub_alternate_trigger.png" alt="" width="563"><figcaption></figcaption></figure>

2. The agent might not trigger after creating a new expense event entry in **x\_snc\_forecast\_v\_0\_expense\_transaction\_event** or throw errors like **Sorry, there was a problem on my side trying to complete this request. Try asking again later.** in Runtime of Flow, Actions, and AI agents > step 8. This can be fixed by doing a dummy change in Custom Forecast Variance AI Agent > Steps 10 to 13; e.g, recreating the trigger.
3. If the Now Assist Agent is not showing the action being executed and the history of chats like below, wait for 5 minutes or so and refresh your browser. This is primarily due to the instance's fresh Now Assist settings which you have just configured earlier.

<figure><img src=".gitbook/assets/sc_common_troubleshoot_now_assist.png" alt=""><figcaption></figcaption></figure>

4. If you get messages in Now Assist from the agent saying messages like below, this just means that indexing of the tables needed by the agent to search transactions is not yet completed. Wait for 10 to 15 minutes.

* Errors/messages in Now Assist below. These do not affect the outcome of your lab activity as the agents and the tools related to this are already configured and is only related to the lab instance server load.
  * There is no available information indicating similar transactions for this vendor in the past based on the cost center being processed.
  * Based on the available information, there is insufficient data to determine whether the results are mostly 'On Target', 'Over Budget', or 'Under Budget.' Please provide additional details or context for a more accurate evaluation.
*   **If the errors persist after waiting 10 to 15 minutes, do the following steps to force an indexing job, but this is not a guaranteed fix if there is a high load in the shared lab ML services used in AI search**.

    * Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Indexed Sources** > <mark style="color:green;">**b.)**</mark> click **AI Search > AI Search Index >** and Ctrl / ⌘ + click **Indexed Sources** to open a new window.

    <figure><img src=".gitbook/assets/sc_common_indexed_sources_nav.png" alt=""><figcaption></figcaption></figure>

    *   Search for **Sources** with the string <mark style="color:green;">**a.)**</mark> \*x\_snc\_forecast then Ctrl / ⌘ + click both <mark style="color:green;">**b.)**</mark> **Cost Center Budget History Indexed Source** and <mark style="color:green;">**c.)**</mark>**&#x20;Expense Transactions Indexed Source** so you have two new windows for these objects.

        <figure><img src=".gitbook/assets/sc_common_search_indexed_sources.png" alt=""><figcaption></figcaption></figure>
    * In the new window for **Center Budget History Indexed Source**, click **Index All Tables**.

    <figure><img src=".gitbook/assets/sc_common_index_budget_history.png" alt=""><figcaption></figcaption></figure>

    *   In the new window for **Expense Transactions Indexed Source**, click **Index All Tables**.

        <figure><img src=".gitbook/assets/sc_common_index_expense_transactions.png" alt=""><figcaption></figcaption></figure>
    * Once done, you can re-execute your agent.

## Conclusion

Congratulations! You have created the **Workflow Data Fabric** integrations that powers the **Financial Forecast Variance Agent** allowing proactive creation of cases based on multiple data sources in a complex landscape to allow proactive management of budgets. Moreover, the AI Agent is triggered as soon as there are changes in the **Expense Transaction Event** table.

## Next step

Let us continue building the data foundations for AI Agents to use. The next suggested exercise is to go deep dive in the data integrations used by the same agent in this exercise - Zero Copy.

[Take me back to main page](./)
