# Lab Exercise: Integration Hub

[Take me back to ReadMe](./)

This lab will walk you through the configuration and usage of Spoke actions and Flows to get expense data from an external source periodically or ad hoc and trigger an agent which will evaluate the expense data and create a Finance case if the involved cost center will be over budget.

There are dedicated Integration Hub and Flow Designer labs so the focus of this exercise is to walk through the configurations in AI Agent Studio and Flow Designer. There is a final exercise at the very end for you to create a Spoke action to provide an understanding on how the AI Agents are triggered.

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

### Walkthrough of Custom Forecast Variance AI Agent

This is a walk through of how the an AI Agent with equipped with both deterministic and probabilistic can automate research and validation of cost center history and expenses as well as creation of Finance Cases should cost centers be above their budget allocations. <mark style="color:red;">**Note:**</mark> this is a custom AI agent pre-configured in the lab instance provided in ServiceNow-led lab sessions; this is not a pre-built agent.

1. Go to All > type **x\_snc\_forecast\_v\_0\_expense\_transaction\_event.list** and hit **Return/Enter ↵**. Ensure that it is empty.
2. If it is not empty, <mark style="color:green;">**a.)**</mark> click on the items > <mark style="color:green;">**b.)**</mark> click Action on selected rows... > <mark style="color:green;">**c.)**</mark> Delete > <mark style="color:green;">**d.)**</mark> Confirm delete. The flow does not have robust exception handling for this lab so this manual step is required to ensure that the scripts will run properly.
3. Navigate to All > <mark style="color:green;">**a.)**</mark> type **AI Agent Studio** > <mark style="color:green;">**b.)**</mark> click on **Create and Manage**.

<figure><img src=".gitbook/assets/sc_ihub_agent_studio.png" alt="" width="334"><figcaption></figcaption></figure>

4. This will go to the list of workflows and agents. Go to **AI agents** tab > <mark style="color:green;">**a.)**</mark> click **search (magnifying glass)** > <mark style="color:green;">**b.)**</mark> type **Forecast Variance** **Integration Hub Trigger** and hit **Return/Enter ↵**.

<figure><img src=".gitbook/assets/sc_ihub_agent_studio_manage.png" alt="" width="563"><figcaption></figcaption></figure>

5. Click on **Forecast Variance Integration Hub Trigger**.

<figure><img src=".gitbook/assets/sc_ihub_forecast_variance_agent.png" alt=""><figcaption></figcaption></figure>

6. Click on **Define the specialty**. This shows all the instructions for this AI Agent created in plain English. The **List of steps** describes the sequence, purpose, and nuances of the tools configured, which are shown in the next section. No further action is required in this section.

<figure><img src=".gitbook/assets/sc_ihub_agent_details_1.png" alt=""><figcaption></figcaption></figure>

7. In the same screen, scroll down to see additional configurations. No further action is required in this section.

<figure><img src=".gitbook/assets/sc_ihub_agent_details_2.png" alt=""><figcaption></figcaption></figure>

8. Next, click on **Add tools and information**. This is a collection of **Search retrievals** and **Subflows** that are used by the agent. The purpose and sequence of these tools are also described in the section **Define the specialty**. No further action is required in this section but feel free to explore the configurations of each of the tools.

<figure><img src=".gitbook/assets/sc_ihub_agent_details_3.png" alt=""><figcaption></figcaption></figure>

9. Next, click on **Define trigger**, which is a key part of this exercise. Click on **Create New Expense Transaction Event** to get a view of how the trigger is configured

<figure><img src=".gitbook/assets/sc_ihub_agent_details_4.png" alt=""><figcaption></figcaption></figure>

10. Notice the details such as the **Select trigger** > **Created** and **Table** > **Expense Transaction Event**. These are set so the AI Agent will be triggered as soon as entries are created in the **Expense Transaction Event** which gets expense data from an external source via REST API.

<figure><img src=".gitbook/assets/sc_ihub_trigger_1.png" alt="" width="563"><figcaption></figcaption></figure>

11. Also notice the configuration for **Conditions** which allows further qualificiation of when the trigger will be activate. The M**ethod for defining sys user** and **Sys\_user** fields are also critical to ensure correct levels of authorizations are used in the trigger.

<figure><img src=".gitbook/assets/sc_ihub_trigger_2.png" alt="" width="563"><figcaption></figcaption></figure>

12. Finally, click on <mark style="color:green;">**a.)**</mark> **Toggle display**. This configures the availability of the AI Agent. I this case, it is enabled and can be accessed using **Now Assist panel** as well as via **Virtual Agents**. No action is required on this section.

<figure><img src=".gitbook/assets/sc_ihub_agent_details_5.png" alt=""><figcaption></figcaption></figure>

### Runtime of Flow, Actions, and AI Agents

1. dd
2. d
3. d
4. d
5. d
6. d
7. d
8. You will be directed to the Test AI reasoning tab. To proceed with testing, <mark style="color:green;">**a.)**</mark> type **Help me process EXP-2025-IT-002-1007-01** and <mark style="color:green;">**b.)**</mark> click **Start test**.

12\. Wait for the test to complete which is indicated by an <mark style="color:green;">**End**</mark> with a check mark. Once that is completed, you can explore the following sections. These automations help assess and review cost centers which are exceeding budget proactively instead of waiting at the end of reporting cycles.

<mark style="color:green;">**a.)**</mark> Expand **Planning the next steps** to see the tools used.

<mark style="color:green;">**b.)**</mark> Note the **cost\_center** and **vendor** extracted from the expense event.

<mark style="color:green;">**c.)**</mark> You can access the result of the **Retrieval-augmented Generation (RAG) search** and click on the links if you wish. This step helps you check relevant entries for the cost center associated with the expense event so you can do further investigation if needed.

<mark style="color:green;">**d.)**</mark> You can also access the **RAG search** results for the vendors associated with the expense event.

<mark style="color:green;">**e.)**</mark> Finally, if the expense event will lead to the associated cost center being over budget, the total cost center expense and the **Finance Case** created for exceeding the budget for further review and action is listed.

<figure><img src=".gitbook/assets/sc_zcc_agent_test_results.png" alt="" width="563"><figcaption></figcaption></figure>

13\. The right panel of the same screen shows the **AI agent decision logs** for debugging purposes.

<figure><img src=".gitbook/assets/sc_ihub_agent_test_debug.png" alt=""><figcaption></figcaption></figure>

14\. Navigate to Workspaces > <mark style="color:green;">**a.)**</mark> type **Finance Operations Workspace** and click on the <mark style="color:green;">**b.)**</mark> workspace with the same name.

<figure><img src=".gitbook/assets/sc_ihub_fow.png" alt="" width="319"><figcaption></figcaption></figure>

15\. For this exercise, we are not impersonating a persona so you remain as the System user.

<figure><img src=".gitbook/assets/sc_zcc_fow_home.png" alt="" width="563"><figcaption></figcaption></figure>

16\. Go to <mark style="background-color:green;">**a.)**</mark> **list (list icon)** > <mark style="color:green;">**b.)**</mark> **Lists** > then the Finance case just created by the AI Agent.

<figure><img src=".gitbook/assets/sc_ihub_fow_navigation.png" alt=""><figcaption></figcaption></figure>

## Conclusion

Congratulations! You have created the Workflow Data Fabric integrations that powered the Financial Forecast Variance Agent.

## Next step

Let us continue building the data foundations for AI Agents to use. The next suggested exercise is the creation of the External Content Connector to SharePoint.

[Take me back to ReadMe](./)
