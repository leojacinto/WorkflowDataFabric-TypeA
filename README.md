# Workflow Data Fabric Lab: Financial Intelligence at Scale

<figure><img src=".gitbook/assets/sc_persona_wdf.png" alt="" width="563"><figcaption></figcaption></figure>

### Before we start - a note from the author and some disclaimers

This lab demonstrates end-to-end integration scenarios that require both ServiceNow platform capabilities and external system connectivity.&#x20;

#### ServiceNow dependencies

Before attempting these exercises, ensure you have access to the following:

| Component Needed                                  | Required version, Zurich Patch 4 recommended |
| ------------------------------------------------- | -------------------------------------------- |
| Zero Copy Connector for SQL                       | 2.0.0                                        |
| Zero Copy Connector for ERP                       | 8.0.14                                       |
| External Content Connectors for SharePoint Online | 4.1.7                                        |
| Workflow Studio                                   | 28.1.4                                       |
| Now Assist Skill Kit                              | 6.0.7                                        |
| MCP Server                                        | 1.0.0                                        |
| MCP Client                                        | 1.0.7                                        |
| Lens                                              | 2.0.0                                        |
| Document Intelligence                             | 7.1.5                                        |
| AI Control Tower                                  | 1.0.1                                        |

#### External system dependencies

∙ Cloud data warehouse with SQL endpoint (e.g., Snowflake, Databricks, BigQuery)\
∙ Document repository (e.g., SharePoint, Google Drive) for External Content Connector scenarios\
∙ Claude Desktop with MCP configuration (for MCP Server lab)\
∙ Sample ERP dataset or equivalent financial data source

#### What if I don’t have all of this?

Each lab is designed to be conceptually valuable even without a fully configured environment. You can:\
∙ Follow along to understand the architectural patterns and configuration steps\
∙ Adapt the exercises to your own data sources and systems\
∙ Use the provided screenshots and sample outputs as reference

#### Guided Lab Sessions

Fully provisioned environments with all dependencies pre-configured are available through ServiceNow-led workshops and enablement sessions. Contact your ServiceNow representative or reach out to the author for availability.

#### About the author

This lab is created by [Leo Francia](https://www.linkedin.com/in/leojmfrancia/), a Data Architect at ServiceNow, and is in no way a ServiceNow official manual. Leo is an active member of the [ServiceNow community](https://www.servicenow.com/community/workflow-data-fabric/ct-p/workflow-data-fabric) and presales organization so do not hesitate to drop him a note. He is also not sure if he should continue to talk about himself in the third person, but please let him be.

### Business motivation

Finance teams discover budget overruns weeks too late. Expense analysis requires manually piecing together data from ERP systems, data warehouses, and SharePoint. By the time finance reacts, small variances become major problems. **ServiceNow Workflow Data Fabric transforms reactive financial management into proactive intelligence**. By unifying data across systems through Zero Copy for SQL and ERP, Global Graph, and AI agents, organizations can:

* **Detect budget issues in real-time** before they escalate
* **Automate financial case creation** enriched with executive guidance and trend analysis
* **Enable self-service insights** through natural language queries in Employee Center
* **Scale financial operations** with AI agents, not headcount

### Persona context

You're a **Data Architect** serving the Finance department. Finance Managers need immediate visibility into budget performance. Cost Center Owners need to understand why they're over budget; with context, not just numbers. **Your mission**: Build an intelligent financial data fabric that connects ServiceNow to external systems, deploys AI agents to detect and analyze budget issues automatically, surfaces executive guidance, and enables self-service analytics through Employee Center and Claude Desktop. You'll solve three critical problems:

1. "We find out about budget overruns too late: can we get real-time alerts?"
2. "Investigation means manually searching expenses, reports, and memos: can you unify this?"
3. "We answer the same questions daily: can employees self-serve?"

### Outcome

By completing this lab, you'll build a production-grade financial intelligence platform demonstrating:

* **Zero Copy integration** with ERP and cloud warehouses (no data duplication)
* **AI agents** that autonomously detect issues, analyze trends, and create contextual cases
* **External Content Connector** bringing executive memos into agent decisions
* **Integration Hub** for real-time expense event processing
* **Lens** and **Document Intelligence** for invoice data capture individually or batch, respectively
* **MCP Server** enabling Claude Code or Desktop to analyze ServiceNow financial data
* **ServiceNow Enterprise Graph** for natural language queries across systems (not yet released!)

You'll master the architectural patterns for transforming siloed enterprise data into unified, intelligent decision-making platforms. **Let's build something intelligent**. 🚀💡

### Table of contents

This lab is divided into 6 exercises with the suggested sequence below. However, the lab environment which deploys these exercises will allow you to complete individual labs in any sequence you prefer.

| Topic                                                                                             | Difficulty   | Suggested duration |
| ------------------------------------------------------------------------------------------------- | ------------ | ------------------ |
| [Workflow Data Fabric Diagrams](0_WDF_Diagrams.md)                                                | N/A          | N/A                |
| [Lab Exercise: Fundamentals](1_Fundamentals.md)                                                   | Basic        | 20 minutes         |
| [Lab Exercise: Zero Copy](2_Zero_Copy.md)                                                         | Intermediate | 1 hour             |
| [Lab Exercise: Integration Hub](3_Integration_Hub.md)                                             | Intermediate | 30 minutes         |
| [Lab Exercise: External Content Connector](4_External_Content_Connector.md)                       | Basic        | 20 minutes         |
| [Lab Exercise: Model Context Protocol Server/Client and AI Control Tower](5_Lens_and_DocIntel.md) | Intermediate | 1 hour             |
| [Lab Exercise: ServiceNow Lens and Document Intelligence](6_MCP_and_AI_Control_Tower.md)          | Intermediate | 30 minutes         |
