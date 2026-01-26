# Lab Exercise: Model Context Protocol Server/Client and AI Control Tower

<mark style="color:red;">**Lab Exercise creation in progress! Content Coming February 2025.**</mark>

[Take me back to main page](./)

This lab will walk you through the configuration and usage of MCP capabilities to interact with ServiceNow either as a client or as a server, allowing end users to interact with the platform as they see fit. As a final step in the series, you will also get a view of how ServiceNow is able to govern AI assets across your landscape using AI Control Tower.

## Data flow

The data flow below shows how ServiceNow provides MCP client and server capabilities as well governance of AI assets.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        ClaudeDesktop[Claude Desktop<br/>+ MCP]
        ControlTower[AI Control<br/>Tower]
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
    class ZCCC,ZCCH,ZCCO,ZCExp zeroCopy
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,Agent3,RAG,NASK,FlowAction,MCPS,MCPC,Lens,DocIntel ai
    class Employee,EC,ControlTower,ClaudeDesktop user

```

[Take me back to main page](./)
