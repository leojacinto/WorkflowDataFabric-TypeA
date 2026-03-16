---
icon: diagram-nested
---

# Data and Flow Diagrams

[Take me back to main page](./)

## Components

Let us first start by breaking down the different components of the lab. The diagram below is a good representation of a tightly integrated ServiceNow landscape that spans various internal ServiceNow components and external data sources. These internal and external components will be used by Flows and AI Agents to provide the automations needed to solve our business problem of managing financial budgets. While the components will look overwhelming, the reality is customer landscapes require this level of complexity to manage different types of data across multiple functions. The key thing to note is the end user will interact with **Workspace**, **Employee Center**, or an **MCP Client** (e.g., Claude Code or Desktop).

### External system prerequisites

Baseline integration to the external systems listed in this lab have mostly been configured.

```mermaid
graph LR
    subgraph "External System Prerequisites"
        ERP[(ERP System<br/>Data)]
        ExpenseAPI[Expense Event<br/>API]
        SharePoint[SharePoint<br/>Executive Memos]
        CDW[(Cloud Data<br/>Warehouse)]
    end

    %% Styling
    classDef external fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff

    class ERP,ExpenseAPI,SharePoint,CDW external
```

* **ERP**: This lab will use an SAP system with either BAPI/RFC or OData endpoints. The authentication and integration is already configured in this exercise and the objective is get the needed data by selecting the ERP data model and extraction table. If you wish to learn more on how to create the configuration in your own environment, check this [Zero Copy Connector for ERP guide by Leo Francia in the ServiceNow community](https://www.servicenow.com/community/app-engine-for-erp-blogs/part-1-of-4-intelligent-erp-workflows-get-sap-data-into/ba-p/3192800). You can also take this ServiceNow University course on [Introduction to Zero Copy Connector for ERP Data Products and Process Extensions](https://learning.servicenow.com/lxp/en/app-engine/introduction-to-zero-copy-connector-for-erp-data-products-and?id=learning_course_prev\&course_id=72e3387d937bea54fb94b4886cba1095).
* **Cloud Data Warehouse**: Snowflake will be the cloud data warehouse used in this lab. If you have a Databricks or Redshift environment, the principles and steps here will also apply. The Snowflake key-pair authentication and integration is already configured in this exercise and the objective is get the needed data asset by selecting it from Workflow Data Fabric Hub. If you wish to learn more on how to create the configuration in your own environment, check this ServiceNow University course on [Zero Copy Connector Basics](https://learning.servicenow.com/lxp/en/automation-engine/zero-copy-connector-basics?id=learning_course_prev\&course_id=c505959493283e903cc0322d6cba1025).
* **Document Storage**: SharePoint will be used as the document storage which will be the target of External Content Connectors or XCC. Unstructured data will be stored in SharePoint which will be indexed by ServiceNow as additional source of data for Flows and AI Agents in this lab exercise. If you wish to learn more on how to create the configuration in your own environment, check this ServiceNow University course on [Introduction to AI Search and External Content Connectors](https://learning.servicenow.com/lxp/en/now-platform/introduction-to-ai-search-and-external-content-connectors?id=learning_course_prev\&course_id=62283c7c93d46e50f2d9bc686cba107b).
* **Expense Event API**: This component can be created as a mock endpoint using services such as [beeceptor.com](https://beeceptor.com/). The specification for the API will be provided in this lab so you can simulate it in your own environment.

### User interaction layer

The end user will interact with **Workspace**, **Employee Center**, or an **MCP Client** (e.g., Claude Code or Desktop). These three interfaces will be end test scenario for the lab exercises.

As of March-2026 version of this lab, MCP Server access through Claude or similar is not yet included.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/>Workspace with Now Assist]
        ClaudeDesktop[Claude Desktop<br/>+ MCP]
    end

    %% Styling
    classDef user fill:#F5F5F5,stroke:#616161,stroke-width:3px,color:#1a1a1a

    class Employee,EC,ClaudeDesktop user
```

### ServiceNow Workflow Data Fabric

The next diagram shows the various ServiceNow components that interact with the external systems while working in the back-end to provide the data and automation needed by users.

```mermaid
graph 
    subgraph "ServiceNow AI Platform"
        spacer[ ]:::hidden
        subgraph "Data Integration Layer"
            ZeroCopySQL[Zero Copy SQL<br/>Connection]
            ZeroCopyERP[Zero Copy ERP<br/>Connection]
            IntHub[Integration Hub<br/>Spoke/Flow]
            ExtContent[External Content<br/>Connector]
            MCP[MCP]
        end

        subgraph "Zero Copy Tables - Read Only"
            ZCCC[(Cost Center)]
            ZCCH[(Cost Center</br>History)]
            ZCCS[(Cost Center</br>Summary)]
            ZCExp[(Expenses)]
        end

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
            FinCase[(Finance Case<br/>Table)]
        end


        subgraph "AI & Automation"
            Agent1[Agent: Over-Budget<br/>Case Creator<br/>Zero Copy Source]
            Agent2[Agent: Proactive<br/>Budget Alert<br/>Integration Hub Source]
            RAG[RAG - Retrieval<br/>Augmented Generation]
            FlowAction[Flow and Action]

        end

        subgraph "AI Experiences"
            Lens["ServiceNow</br>Lens"]
            DocIntel["Document</br>Intelligence"]
        end
    end

    %% Styling
    classDef external fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef user fill:#F5F5F5,stroke:#616161,stroke-width:3px,color:#1a1a1a
    classDef nowassist fill:#FFB300,stroke:#F57F17,stroke-width:2px,color:#1a1a1a
    classDef platform fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef wdf fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef hidden fill:none,stroke:none,color:transparent,font-size:0

    class ZeroCopySQL,ZeroCopyERP,IntHub,ExtContent wdf
    class ZCCC,ZCCH,ZCCS,ZCExp wdf
    class ExpenseTable,FinCase platform
    class FlowAction platform
    class Agent1,Agent2,RAG nowassist
    class MCP wdf
    class Lens,DocIntel nowassist
```

> **Color Legend:** 🟡 Now Assist | 🟢 Platform | 🟣 Workflow Data Fabric

#### Data Integration Layer and Zero Copy Tables

These data integrations match the external sources mentioned earlier.

* **Integration Hub**: will access the REST API data, for the lab it will be a periodic trigger.
* **Zero Copy Connector for ERP**: also known as ZCC for ERP will get the cost center master data from SAP.
* **Zero Copy Connector for SQL**: also known as ZCC for SQL will connect to the Snowflake data assets for the lab, specifically the Cost Center History, Expenses, and Summary.
* **External Content Connector**: will access the indexed documents in SharePoint to enrich decision making and automations for our finance workflow.

#### Zero Copy Tables

These are pointers to the respective tables coming from either the Cloud Data Warehouse (Snowflake) or ERP (SAP).

* **Cost Center Master Data:** taken from the ERP system, known as CSKS from SAP, which can be obtained via BAPI, RFC Table Read, or OData endpoints. Master data does not change frequently in ERP systems so either persistence or zero copy approaches are viable for ServiceNow use cases.
* **Cost Center Summary**: aggregated Cost Center History data for the year stored in the Cloud Data Warehouse for reporting purposes.
* **Cost Center History**: monthly data taken from the Cloud Data Warehouse with information whether cost centers have historically gone over/under budget or on target. ERP systems normally do not store this type of history or aggregation and is hence stored in a business or data warehouse. **Note** that for the purpose of this exercise, this has been created as a local ServiceNow table but is usually stored in a Cloud Data Warehouse or ERP system in customer environments.
* **Expense History**: this can come from an expense management system, ERP system, or Cloud Data Warehouse. For this lab, we are obtaining this from the Cloud Data Warehouse. **Note** that for the purpose of this exercise, this has been created as a local ServiceNow table but is usually stored in a Cloud Data Warehouse or ERP system in customer environments.

#### ServiceNow Native Tables

These are local tables and are not persisted in any other systems.

* **Expense Event Table:** is a scoped table will obtain expense events via Rest API from expense sources such as cloud infrastructure services or even document capture via ServiceNow Lens and Document Intelligence.
* **Finance Case Table**: is a standard table in ServiceNow Finance case management (**sn\_spend\_sdc\_service\_request**) where the Flows and Agents will perform updates based on the expense events ingested either in the background or interactively.

#### AI & Automation

* **Flow and Action:** a scoped Flow and a scoped Action are used to get expense data from a REST API source.
* **MCP Server and Client:** MCP or Model Context Protocol is an open standard that lets AI models (LLMs) securely connect to and use external data, tools, and services, acting like a universal adapter to give real-world context beyond their training data for better decision-making and task execution. This will allow Now Assist from ServiceNow act as a data source for clients such as Claude Desktop or act as a client when connecting to MCP-based services (e.g. Snowflake or Notion) feeding data into Flows or Agents.
* **RAG - Retrieval Augmented Generation:** Now Assist uses AI Search to retrieve relevant information from your knowledge bases, documentation, and records before generating a response. Rather than relying solely on what the LLM was trained on, it grounds answers in your actual ServiceNow local and integrated data. Think of it as having someone who does the research first, then answers, except it happens in seconds.
* **Agent: Proactive Budget Alert Integration Hub Source:** contains RAG and Flows to assess cost center budget history, transactions, and status to create the appropriate Finance Case so budgets can be handled proactively. This is triggered by the Flow and Action that gets Expense Transaction Events from an external REST API source.
* **Agent: Over-Budget Case Creator Zero Copy Source**: similar to **Agent: Proactive Budget Alert Integration Hub Source** but does not have a trigger. This agent is created separately to create a lab exercise that focuses on Zero Copy but is similar to **Agent: Proactive Budget Alert Integration Hub Source** with the only difference being the trigger configuration.

#### AI Experiences

While not part of Workflow Data Fabric, these provide additional data sources for the Flows and AI Agents to use.

* **ServiceNow Lens:** an AI-powered feature that uses generative AI to scan, extract, and understand data from on-screen sources like screenshots, emails, or log files, even outside ServiceNow. This can be useful to get Expense Transaction Events coming from receipts which are scanned interactively (i.e. through ServiceNow app or in a browser window).
* **Document Intelligence:** an AI-powered solution that uses machine learning, natural language processing (NLP), and computer vision to automatically extract, classify, and process data from various digital and scanned documents, useful for processing Expense Transaction Events coming from multiple documents.

## Overall data flow

The diagram below will be further decomposed in the next sections to give you more detail on the inner workings within ServiceNow while, as mentioned earlier, the end user interacts with **Employee Center**, an **MCP Client** (e.g., Claude Code or Desktop), or in slightly more technical scenarios **AI Control Tower**.

You can skip the review of the diagram below if you prefer, and head straight into the lab exercises, each of which having its individual (and much more detailed) data flow.

```mermaid fullWidth="true"
---
title: Workflow Data Fabric Landscape
---
graph TB
    subgraph USER["User Interaction"]
        WC["Workspace"]
        EC["Employee Center"]
        MCP_C["MCP Client"]
    end

    subgraph SNOW["ServiceNow AI Platform"]
        direction TB
        subgraph AI["AI & Automation"]
            AGENTS["AI Agents"]
            FLOWS["Flows & Actions"]
            RAG["RAG via AI Search"]
        end
        subgraph INT["Integration Layer"]
            ZCC["Zero Copy<br/>Connectors"]
            INTHUB["Integration<br/>Hub"]
            XCC["External Content<br/>Connector"]
            MCP_S["MCP"]
        end
        subgraph DATA["Data Layer"]
            ZCT["Zero Copy Tables"]
            NT["Native Tables"]
        end
        subgraph AX["AI Experiences"]
            LENS["Lens"]
            DOCINT["Document Intelligence"]
        end
    end

    subgraph EXT["External Systems"]
        ERP["ERP"]
        CDW["Cloud Data Warehouse"]
        DOC["Document Storage"]
        API["Expense Event API"]
        EXT_MCP["External MCP"]
    end

    USER --> AI
    MCP_C --> MCP_S
    AI --> DATA
    AX --> DATA
    DATA --> ZCC
    ZCC --> ERP
    ZCC --> CDW
    AI --> INTHUB
    INTHUB --> API
    AI --> XCC
    XCC --> DOC
    MCP_S --> EXT_MCP

    %% Styling
    classDef external fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef user fill:#F5F5F5,stroke:#616161,stroke-width:3px,color:#1a1a1a
    classDef nowassist fill:#FFB300,stroke:#F57F17,stroke-width:2px,color:#1a1a1a
    classDef platform fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef wdf fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff

    class ERP,CDW,DOC,API,EXT_MCP external
    class ZCC,INTHUB,XCC,MCP_S wdf
    class ZCT wdf
    class NT platform
    class AGENTS,RAG nowassist
    class FLOWS platform
    class LENS,DOCINT nowassist
    class WC,EC,MCP_C user
```

> **Color Legend:** 🟡 Now Assist | 🟢 Platform | 🟣 Workflow Data Fabric | 🔵 External Systems | ⚪ User Interaction

[Take me back to main page](./)
