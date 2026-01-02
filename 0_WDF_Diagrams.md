# Data and Flow Diagrams

## Components

Let us first start by breaking down the different components of the lab. In a tightly integrated ServiceNow landscape that spans various internal ServiceNow components and external data sources, the diagram below would be a good represenation. These internal and external components will be used by Flows and AI Agents to provide the automations needed to solve our business problem of managing financial budgets. While the components will look overwhelming, the reality is customer landscapes require this level of complexity to manage different types of data across multiple functions. The key thing to note is the end user will interact with **Employee Center**, an **MCP Client** (e.g., Claude Code or Desktop), or in slightly more technical scenarios **AI Control Tower**.

### External system prerequisites

Baseline configuration for the external systems listed in this lab are done prior to the steps listed. As mentioned in the disclaimer, environments which will have the prereqiusite external systems will be available externally for customers soon and for time being, you can use this lab as a guide on how the components will interact.

```mermaid
graph LR
    subgraph "External System Prerequisites"
        ERP[(ERP System<br/>Data)]
        ExpenseAPI[Expense Event<br/>API]
        SharePoint[SharePoint<br/>Executive Memos]
        CDW[(Cloud Data<br/>Warehouse)]
    end

    %% Styling
    classDef external fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef integration fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef zeroCopy fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef native fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef user fill:#e3f2fd,stroke:#1565c0,stroke-width:3px

    class ERP,ExpenseAPI,SharePoint,CDW external
    class ZeroCopySQL,ZeroCopyERP,IntHub,ExtContent integration
    class ZCCC,ZCCH,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,RAG,NASK,FlowAction,MCP,MCPC,GGraph,NLQuery,Lens,DocIntel ai
    class Employee,EC,ControlTower,ClaudeDesktop user
```

* **ERP**: This lab will use an SAP system with either BAPI/RFC or OData endpoints. The authentication and integration is already configured in this exercise and the objective is get the needed data by selecting the ERP data model and extraction table. If you wish to learn more on how to create the configuration in your own environment, check this [Zero Copy Connector for ERP guide from Leo Francia in the ServiceNow community](https://www.servicenow.com/community/app-engine-for-erp-blogs/part-1-of-4-intelligent-erp-workflows-get-sap-data-into/ba-p/3192800). You can also take this ServiceNow University course on [Introduction to Zero Copy Connector for ERP Data Products and Process Extensions](https://learning.servicenow.com/lxp/en/app-engine/introduction-to-zero-copy-connector-for-erp-data-products-and?id=learning_course_prev\&course_id=72e3387d937bea54fb94b4886cba1095).
* **Cloud Data Warehouse**: Snowflake will be the cloud data warehouse used in this lab. If you have a Databricks or Redshift environment, the principles and steps here will also apply. The Snowflake key-pair authentication and integration is already configured in this execrcise and the objective is get the needed data asset by selecting it from Workflow Data Fabric Hub. If you wish to learn more on how to create the configuration in your own environment, check this ServiceNow University course on [Zero Copy Connector Basics](https://learning.servicenow.com/lxp/en/automation-engine/zero-copy-connector-basics?id=learning_course_prev\&course_id=c505959493283e903cc0322d6cba1025).
* **Document Storage**: SharePoint will be used as the document storage which will be the target of External Content Connectors or XCC. Unstructured data will be stored in SharePoint which will be indexed by ServiceNow as additional source of data for Flows and AI Agents in this lab exercise. If you wish to learn more on how to create the configuration in your own environment, check this ServiceNow University course on [Introduction to AI Search and External Content Connectors](https://learning.servicenow.com/lxp/en/now-platform/introduction-to-ai-search-and-external-content-connectors?id=learning_course_prev\&course_id=62283c7c93d46e50f2d9bc686cba107b).
* **Expense Event API**: This component can be created as a mock endpoint using services such as [beeceptor.com](beeceptor.com). The specification for the API will be provided in this lab so you can simulate it in your own environment.

### User interaction layer

The end user will interact with **Employee Center**, an **MCP Client** (e.g., Claude Code or Desktop), or in slightly more technical scenarios **AI Control Tower**. These three interfaces will be end test scenario for the lab exercises.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/>Workspace with Now Assist]
        ClaudeDesktop[Claude Desktop<br/>+ MCP]
        ControlTower[AI Control<br/>Tower]
    end

    %% Styling
    classDef external fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef integration fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef zeroCopy fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef native fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef user fill:#e3f2fd,stroke:#1565c0,stroke-width:3px

    class ERP,ExpenseAPI,SharePoint,CDW external
    class ZeroCopySQL,ZeroCopyERP,IntHub,ExtContent integration
    class ZCCC,ZCCH,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,RAG,NASK,FlowAction,MCP,MCPC,GGraph,NLQuery,Lens,DocIntel ai
    class Employee,EC,ControlTower,ClaudeDesktop user
```

### ServiceNow Workflow Data Fabric

The next diagram shows tha various ServiceNow components that interact with the external systems while working in the back-end to provide the data and automation needed by users.

```mermaid
graph LR
    subgraph "ServiceNow Workflow Data Fabric"
        subgraph "Data Integration Layer"
            ZeroCopySQL[Zero Copy SQL<br/>Connection]
            ZeroCopyERP[Zero Copy ERP<br/>Connection]
            IntHub[Integration Hub<br/>Spoke/Flow]
            ExtContent[External Content<br/>Connector]
        end

        subgraph "Zero Copy Tables - Read Only"
            ZCCC[(Cost Centre)]
            ZCCH[(Cost Centre History)]
            ZCExp[(Expenses)]
        end

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
            FinCase[(Finance Case<br/>Table)]
            FinVar[(Finance Variance<br/>Table)]
        end

        subgraph "ServiceNow Enterprise Graph"
            GGraph[ServiceNow Enterprise<br/>Graph Schema]
            NLQuery[Natural Language<br/>Query Interface]
        end

        subgraph "AI & Automation"
            Agent1[Agent: Over-Budget<br/>Case Creator<br/>Zero Copy Source]
            Agent2[Agent: Proactive<br/>Budget Alert<br/>Integration Hub Source]
            RAG[RAG - Retrieval<br/>Augmented Generation]
            NASK[NASK - Now Assist<br/>Skill Kit]
            FlowAction[Flow Action]
            MCP[MCP Server]
            MCPC[MCP Client]
        end

        subgraph "AI Experiences"
            Lens["ServiceNow</br>Lens"]
            DocIntel["Document</br>Intelligence"]
        end
    end

    %% Styling
    classDef external fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef integration fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef zeroCopy fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef native fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef user fill:#e3f2fd,stroke:#1565c0,stroke-width:3px

    class ERP,ExpenseAPI,SharePoint,CDW external
    class ZeroCopySQL,ZeroCopyERP,IntHub,ExtContent integration
    class ZCCC,ZCCH,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,RAG,NASK,FlowAction,MCP,MCPC,GGraph,NLQuery,Lens,DocIntel ai
    class Employee,EC,ControlTower,ClaudeDesktop user
```

#### Data Integration Layer and Zero Copy Tables

These data integrations match the external sources mentioned earlier.

* **Zero Copy Connector for SQL**: also known as ZCC for SQL will connect to the Snowflake data assets for the lab, specifically the Cost Center History, Expenses, and Summary.
* **Zero Copy Connector for ERP**: also known as ZCC for ERP will get the cost center master data from SAP.
* **Integration Hub**: will access the REST API data, for the lab it will be a periodic trigger.
* **External Content Connector**: will access the indexed documents in SharePoint to enrich decision making and automations for our finance workflow.

## Overall data flow

Do not let the chart intimidate you 😉. This will be broken down further and the intent of showing the whole data flow is to provide an overview of the inner workings within ServiceNow while, as mentioned earlier, the end user will interact with **Employee Center**, an **MCP Client** (e.g., Claude Code or Desktop), or in slightly more technical scenarios **AI Control Tower**.

You can skip the review of the diagram below if you prefer and head straight into the lab exercises if you so desire with the data flow and their respective labs broken down below.

* [Lab Exercise: Fundamentals](1_Fundamentals.md)
* [Lab Exercise: Integration Hub](3_Integration_Hub.md)
* [Lab Exercise: Zero Copy Connectors](2_Zero_Copy.md)
* [Lab Exercise: External Content Connector](4_External_Content_Connector.md)
* [Lab Exercise: ServiceNow Lens and Document Intelligence](6_MCP_and_AI_Control_Tower.md)
* [Lab Exercise: Model Context Protocol Server/Client and AI Control Tower](5_Lens_and_DocIntel.md)

```mermaid fullWidth="true"
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/>Workspace with Now Assist]
        ClaudeDesktop[Claude Desktop<br/>+ MCP]
        ControlTower[AI Control<br/>Tower]
    end

    subgraph "External Systems"
        ERP[(ERP System<br/>Data)]
        ExpenseAPI[Expense Event<br/>API]
        SharePoint[SharePoint<br/>Executive Memos]
        CDW[(Cloud Data<br/>Warehouse)]
    end

    subgraph "AI Experiences"
        Lens["ServiceNow</br>Lens"]
        DocIntel["Document</br>Intelligence"]
    end

    subgraph "ServiceNow Workflow Data Fabric"
        subgraph "Data Integration Layer"
            ZeroCopySQL[Zero Copy SQL<br/>Connection]
            ZeroCopyERP[Zero Copy ERP<br/>Connection]
            IntHub[Integration Hub<br/>Spoke/Flow]
            ExtContent[External Content<br/>Connector]
        end

        subgraph "Zero Copy Tables - Read Only"
            ZCCC[(Cost Centre)]
            ZCCH[(Cost Centre History)]
            ZCExp[(Expenses)]
        end

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
            FinCase[(Finance Case<br/>Table)]
            FinVar[(Finance<br/>Variance Table)]
        end


        subgraph AI[AI & Automation]
            Agent1[Agent: Over-Budget<br/>Case Creator<br/>Zero Copy Source]
            Agent2[Agent: Proactive<br/>Budget Alert<br/>Integration Hub Source]
            RAG[RAG - Retrieval<br/>Augmented Generation]
            NASK[NASK - Now Assist<br/>Skill Kit]
            FlowAction[Flow Action]
            MCPS[MCP Server]
            MCPC[MCP Client]
        end
    end

    %% Data Flow Connections
    ERP -->|OData Feed| ZeroCopyERP
    CDW -->|Data Fabric table| ZeroCopySQL

    ZeroCopyERP --> ZCCC
    ZeroCopySQL --> ZCCH
    ZeroCopySQL --> ZCExp
    ExpenseAPI -->|Real-time Events| IntHub
    IntHub -->|Write| ExpenseTable
    EC -->|Individual UI-based| Lens -->|Write| ExpenseTable
    EC -->|Individual UI-based| DocIntel -->|Write| ExpenseTable
    SharePoint -->|Executive Guidance| ExtContent

    %% Agent 1 Workflow - Zero Copy Source
    ZCCC -->|Query Over-Budget| Agent1
    ZCCH -->|Historical Data| Agent1
    ZCExp -->|Expense Details| Agent1
    ExpenseTable -->|Search Similar Cases| Agent1
    ZCExp -->|Search Similar Cases| Agent1
    ExtContent -->|Executive Context| Agent1
    Agent1 -->|Create Case| FinCase
    Agent1 <-->|Trend Analysis| RAG
    Agent1 <-->|Knowledge Retrieval| NASK
    Agent1 <-->|Flows/Subflows/Actions| FlowAction
    Agent1 -->|Record Variance| FinVar

    %% Agent 2 Workflow - Integration Hub Source
    ExpenseTable -->|Incoming Event| Agent2
    ZCCC -->|Current Budget| Agent2
    Agent2 -->|Search Similar Cases| FinCase
    ExtContent -->|Executive Context| Agent2
    Agent2 -->|Create Alert Case| FinCase
    Agent2 -->|Record Variance| FinVar

    %% MCP Server Connection
    FinVar -->|Query Data| MCPS
    FinCase -->|Query Data| MCPS
    MCPS <-->|API Communication| ClaudeDesktop

    %% MCP Client Connection
    Agent1 -->|Query Data| MCPC
    MCPC -->|Query Data| CDW

    %% User Interaction Connections
    Employee -->|Ask Questions<br/>View/Update Cases| EC
    EC -->|Search & Query| FinCase
    Employee -->|Access| ControlTower -->|Govern| AI
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
    class ZCCC,ZCCH,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,RAG,NASK,FlowAction,MCPS,MCPC,GGraph,NLQuery,Lens,DocIntel ai
    class Employee,EC,ControlTower,ClaudeDesktop user
```
