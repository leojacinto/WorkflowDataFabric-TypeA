# Lab Exercise: Zero Copy Connectors

[Take me back to ReadMe](./)

This lab will walk you through integration of data coming from Cloud Data Warehouses and ERP using Zero Copy Connectors (ZCC) for SQL and ERP respectively.

### Data flow

The data flow below shows how ServiceNow will consume Cloud Data Warehouse Data Assets and ERP OData Endpoints via ZCC for SQL and ERP respectively. The data taken from the external sources will be used by an agent which is triggered periodcially and will create Finance Cases for Cost Centers which are going overbudget. While majority of the workflow is handled deterministically, AI Agents will provide additional context by searching and comparing expenses and cost center histories to enrich the workflow data that will be used by the personnel in charge of the cost centers.

**Note**: future versions of this lab will include ServiceNow Enterprise Graph which will provide a universal query functionality that brings together the various internal and external data sources. As of Jan-2026, said feature is not globally available and is hence not yet included in this lab.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/> Workspace with Now Assist]
    end

    subgraph "External Systems"
        ERP[(ERP System<br/>OData Endpoint)]
        CDW[(Cloud Data<br/>Warehouse)]
    end

    subgraph "ServiceNow Workflow Data Fabric"
        subgraph "Data Integration Layer"
            ZeroCopySQL[Zero Copy SQL<br/>Connection]
            ZeroCopyERP[Zero Copy ERP<br/>Connection]
        end

        subgraph "Zero Copy Tables - Read Only"
            ZCCC[(Cost Centre)]
            ZCCH[(Cost Centre</br>History)]
            ZCExp[(Expenses)]
        end

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
            FinCase[(Finance Case<br/>Table)]
            FinVar[(Finance<br/>Variance Table)]
        end

        subgraph "AI & Automation"
            Agent1[Agent: Over-Budget<br/>Case Creator<br/>Zero Copy Source]
            RAG[RAG - Retrieval<br/>Augmented Generation]
            NASK[NASK - Now Assist<br/>Skill Kit]
            FlowAction[Flow Action]
        end
    end

    %% Data Flow Connections
    ERP -->|OData Feed| ZeroCopyERP
    CDW -->|Data Fabric table| ZeroCopySQL
    ZeroCopyERP --> ZCCC
    ZeroCopySQL --> ZCCH
    ZeroCopySQL --> ZCExp

    %% Agent 1 Workflow - Zero Copy Source
    ZCCC -->|Query Over-Budget| Agent1
    ZCCH -->|Historical Data| Agent1
    ZCExp -->|Expense Details| Agent1
    ExpenseTable -->|Search Similar Cases| Agent1
    ZCExp -->|Search Similar Cases| Agent1
    Agent1 -->|Create Case| FinCase
    Agent1 <-->|Trend Analysis| RAG
    Agent1 <-->|Knowledge Retrieval| NASK
    Agent1 <-->|Flows/Subflows/Actions| FlowAction
    Agent1 -->|Record Variance| FinVar

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

    class ERP,SharePoint,CDW external
    class ZeroCopySQL,ZeroCopyERP,ExtContent integration
    class ZCCC,ZCCH,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,RAG,NASK,FlowAction,GGraph,NLQuery ai
    class MockERP,MockCDW external
    class Employee,EC user
```

### Steps

#### Zero Copy for SQL

1. Test
<img src=".gitbook/assets/sc_zcc_snowflake.png" alt="" width="400">
2. a
<img src=".gitbook/assets/sc_zcc_wdf_hub.png" alt="" width="400">
3. a
<img src=".gitbook/assets/sc_zcc_wdf_hub_landing.png" alt="" width="400">
4. a
<img src=".gitbook/assets/sc_zcc_snowflake_connection.png" alt="" width="400">
5. a
<img src=".gitbook/assets/sc_zcc_data_asset.png" alt="" width="400">
6. a
<img src=".gitbook/assets/sc_zcc_df_table.png" alt="" width="400">
7. a
<img src=".gitbook/assets/sc_zcc_columns.png" alt="" width="400">
8. a
<img src=".gitbook/assets/sc_zcc_select_columns.png" alt="" width="400">
9. a
<img src=".gitbook/assets/sc_zcc_cc_reference.png" alt="" width="400">
10. a
<img src=".gitbook/assets/sc_zcc_reference_table.png" alt="" width="400">
11. a
<img src=".gitbook/assets/sc_zcc_reference_key.png" alt="" width="400">
12. a
<img src=".gitbook/assets/sc_zcc_reference_label.png" alt="" width="400">
13. a
<img src=".gitbook/assets/sc_zcc_finalize_df.png" alt="" width="400">
14. a
<img src=".gitbook/assets/sc_zcc_confirm_pk.png" alt="" width="400">
15. a
<img src=".gitbook/assets/sc_zcc_df_completed.png" alt="" width="400">
16. a
<img src=".gitbook/assets/sc_zcc_view_df.png" alt="" width="400">
17. a
<img src=".gitbook/assets/sc_zcc_show_df.png" alt="" width="400">
18. a
<img src=".gitbook/assets/sc_zcc_df_reference.png" alt="" width="400">
19. a
<img src=".gitbook/assets/sc_zcc_sap_cc_ref.png" alt="" width="400">

[Take me back to ReadMe](./)
