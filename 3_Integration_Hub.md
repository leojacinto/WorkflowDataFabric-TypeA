# Lab Exercise: Integration Hub

[Take me back to ReadMe](./)

This lab will walk you through configuration of Spoke actions and Flows to get expense data from an external source periodically or ad hoc and trigger an agent which will evaluate the expense data and create a Finance case if the involved cost center will be over budget.

### Data flow

The data flow below shows how ServiceNow will consume REST API endpoints via Integration Hub Spokes then further processed by a Flow so the entries will be written in the scoped table.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/> Workspace with Now Assist]
    end

    subgraph "External Systems"
        ExpenseAPI[Expense Event<br/>API]
        SharePoint[SharePoint<br/>Executive Memos]
    end

    subgraph "ServiceNow Workflow Data Fabric"
        subgraph "Data Integration Layer"
            IntHub[Integration Hub<br/>Spoke/Flow]
            ExtContent[External Content<br/>Connector]
        end

        subgraph "Zero Copy Tables - Read Only"
            ZCCC[(Cost Centre)]
        end

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
            FinCase[(Finance Case<br/>Table)]
            FinVar[(Financial Variance<br/>Table)]
        end

        subgraph "AI & Automation"
            Agent2[Agent: Proactive<br/>Budget Alert<br/>Integration Hub Source]
        end
    end

    subgraph "Lab Prerequisites - Mock Services"
        MockExpense[Mock Expense<br/>Event Service]
    end

    %% Data Flow Connections
    ExpenseAPI -->|Real-time Events| IntHub
    MockExpense -.->|Lab Simulation| IntHub
    IntHub -->|Write| ExpenseTable

    SharePoint -->|Executive Guidance| ExtContent

    %% Agent 2 Workflow - Integration Hub Source
    ExpenseTable -->|Incoming Event| Agent2
    ZCCC -->|Current Budget| Agent2
    Agent2 -->|Search Similar Cases| FinCase
    ExtContent -->|Executive Context| Agent2
    Agent2 -->|Create Alert Case| FinCase
    Agent2 -->|Record Variance| FinVar

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
    class Agent2,NLQuery ai
    class MockExpense external
    class Employee,EC user
```

[Take me back to ReadMe](./)
