# Lab Exercise: External Content Connector
[Take me back to ReadMe](https://github.com/leojacinto/WorkflowDataFabric/blob/main/ReadMe.md)
<span style="color: red;">Lab Exercise coming soon!</span>
This lab will walk you through configuration of External Content Connectors as a source of unstructured document data to supplement automations needed in Finance case creation.
### Data Flow
The data flow below shows how ServiceNow will infomration from indexed documents from a document repository such as SharePoint to provide additional context and information to assist with Flows and Automations.
```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/> Workspace with Now Assist]
    end

    subgraph "External Systems"
        SharePoint[SharePoint<br/>Executive Memos]
    end

    subgraph "ServiceNow Workflow Data Fabric"
        subgraph "Data Integration Layer"
            ExtContent[External Content<br/>Connector]
        end

        subgraph "ServiceNow Native Tables"
            FinCase[(Finance Case<br/>Table)]
        end
    end

    %% Data Flow Connections
    SharePoint -->|Executive Guidance| ExtContent

    %% User Interaction Connections
    Employee -->|Ask Questions<br/>View/Update Cases| EC
    EC -->|Search & Query| FinCase
    EC -->|Natural Language| ExtContent

    %% Styling
    classDef external fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef integration fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef native fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef user fill:#e3f2fd,stroke:#1565c0,stroke-width:3px

    class SharePoint external
    class ExtContent integration
    class FinCase native
    class Employee,EC user
```
[Take me back to ReadMe](https://github.com/leojacinto/WorkflowDataFabric/blob/main/ReadMe.md)
