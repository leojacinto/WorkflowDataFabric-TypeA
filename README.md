# Workflow Data Fabric Lab: Financial Intelligence at Scale

<figure><img src=".gitbook/assets/sc_persona_wdf.png" alt="" width="563"><figcaption></figcaption></figure>

## Business motivation

Finance teams discover budget overruns weeks too late. Expense analysis requires manually piecing together data from ERP systems, data warehouses, and SharePoint. By the time finance reacts, small variances become major problems. **ServiceNow Workflow Data Fabric transforms reactive financial management into proactive intelligence**. By unifying data across systems through Zero Copy for SQL and ERP, Spokes, External Content Connectors, MCP, and AI agents, organizations can:

* **Detect budget issues in real-time** before they escalate
* **Automate financial case creation** enriched with executive guidance and trend analysis
* **Enable self-service insights** through natural language queries in Employee Center
* **Scale financial operations** with AI agents, not headcount

Your automations and AI Agents are just as good as your underlying data. Integrations powered by Workflow Data Fabric allow AI Agents to automate critical processes using accurate and consistent data.

With the trend of external agents reaching through enterprise data, it is worth examining why platform-native agents can scale more safely. Agents built within ServiceNow inherit battle-tested authorization models: role-based access, ACLs, and purpose-built security controls for AI agents; allowing organizations to automate confidently without stepping outside their governance boundaries.

## Persona context

You're a **Data Architect** serving the Finance department. Finance Managers need immediate visibility into budget performance. Cost Center Owners need to understand why they're over budget; with context, not just numbers. **Your mission**: Build an intelligent financial data fabric that connects ServiceNow to external systems, deploys AI agents to detect and analyze budget issues automatically, surfaces executive guidance, and enables self-service analytics through Employee Center and Claude Desktop. You'll solve three critical problems:

1. "We find out about budget overruns too late: can we get real-time alerts?"
2. "Investigation means manually searching expenses, reports, and memos: can you unify this?"
3. "We answer the same questions daily: can employees self-serve?"

## Outcome

By completing this lab, you'll build a production-grade financial intelligence platform demonstrating:

* **Integration Hub** for real-time expense event processing
* **Zero Copy integration** with ERP and cloud warehouses (no data duplication)
* **MCP Server** enabling Claude Code or Desktop to analyze ServiceNow financial data
* **AI agents** that autonomously detect issues, analyze trends, and create contextual cases
* <mark style="color:$warning;">**\[Controlled Lab]**</mark>**&#x20;External Content Connector** bringing executive memos into agent decisions
* <mark style="color:$warning;">**\[Roadmap]**</mark>**&#x20;Lens and Document Intelligence** for invoice data capture individually or batch, respectively

You'll master the architectural patterns for transforming siloed enterprise data into unified, intelligent decision-making platforms. **Let's build something intelligent**. 🚀💡

## Table of contents

This lab is divided into 5 exercises with the suggested sequence below. The ServiceNow-led lab environments which contains these exercises will allow you to complete individual labs in any sequence you prefer. The exercises focus on walk through and basic configuration of Workflow Data Fabric integrations and there are pre-made custom agents that make use of the integrations to demonstrate what is possible. You will not need to configure agents in this exercise but steps are provided on how you can explore how the agents were configured.

<table><thead><tr><th width="203.09375">Topic</th><th width="180.48828125">Difficulty</th><th>AI Agents involved</th><th>Suggested duration</th></tr></thead><tbody><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/0_wdf_diagrams">Workflow Data Fabric Diagrams</a></td><td>N/A</td><td>No</td><td>N/A</td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/1_fundamentals">Lab Exercise: Fundamentals</a></td><td>Basic</td><td>No</td><td>30 minutes</td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/2_integration_hub">Lab Exercise: Integration Hub</a></td><td>Basic</td><td>Yes</td><td>45 minutes</td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/3_zero_copy">Lab Exercise: Zero Copy Connectors</a></td><td>Intermediate</td><td>Yes</td><td>1 hour</td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/6_mcp_and_ai_control_tower">Lab Exercise: Model Context Protocol Server/Client</a></td><td>Intermediate</td><td>Yes</td><td>1 hour</td></tr><tr><td><mark style="color:$warning;"><strong>[Controlled Lab]</strong></mark> <a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/4_external_content_connector">Lab Exercise: External Content Connector</a></td><td>Basic</td><td>Yes</td><td>20 minutes</td></tr><tr><td><mark style="color:$warning;"><strong>[Roadmap]</strong></mark> <a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/5_lens_and_docintel">Lab Exercise: ServiceNow Lens and Document Intelligence</a></td><td>Intermediate</td><td>Yes</td><td>30 minutes</td></tr></tbody></table>

## Recommended materials

Below is a list of recommended courses that you can read up on to learn more about Workflow Data Fabric.

<table><thead><tr><th width="203.09375">Course</th><th width="180.48828125">Level</th><th>Type</th><th>Duration</th></tr></thead><tbody><tr><td><a href="https://learning.servicenow.com/lxp/en/automation-engine/suite-certification-workflow-data-fabric?id=learning_path_prev&#x26;path_id=668f6e1497069250e4fb72de2153af9d" target="_blank">Workflow Data Fabric</a></td><td>Advanced</td><td>Learning Path</td><td>4 days, 2 hours</td></tr><tr><td><a href="https://learning.servicenow.com/lxp/en/automation-engine/sprint-to-workflow-data-fabric-suite-certification?id=learning_course_prev&#x26;course_id=6862722387102e905aa9ca2d0ebb3591" target="_blank">Sprint to Workflow Data Fabric Suite Certification</a></td><td>Advanced</td><td>Course</td><td>2 days, 5 hours</td></tr></tbody></table>

## A note from the author and some disclaimers

This lab involves integrating ServiceNow with external systems (e.g., databases, APIs, cloud services). Some steps require pre-configured environments and connectivity that may not be available in a standard PDI; this best run as a guided workshop.

### ServiceNow dependencies

Before attempting these exercises, ensure you have access and license entitlements to the following:

| Component needed                                  | Required version, Zurich Patch 4 recommended |
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

### External system dependencies

* Cloud data warehouse with SQL endpoint (e.g., Snowflake, Databricks, BigQuery)
* Claude Desktop with MCP configuration (for MCP Server lab)
* Sample ERP dataset or equivalent financial data source

### What if I don’t have all of this?

Each lab is designed to be conceptually valuable even without a fully configured environment. You can:

* Follow along to understand the architectural patterns and configuration steps
* Adapt the exercises to your own data sources and systems
* Use the provided screenshots and sample outputs as reference

### Guided lab sessions and object dependencies

Fully provisioned environments with all dependencies pre-configured are available through ServiceNow-led workshops and enablement sessions. Please note that this lab uses the latest ServiceNow components as well as custom AI Agents and scoped objects, so provisioning requires lead time. Contact your ServiceNow representative or reach out to the author for availability.

### About the author

This lab is created by <a href="https://www.linkedin.com/in/leojmfrancia/" target="_blank">Leo Francia</a>, a Data Architect at ServiceNow, and is in no way a ServiceNow official manual. Leo is an active member of the <a href="https://www.servicenow.com/community/workflow-data-fabric/ct-p/workflow-data-fabric" target="_blank">ServiceNow community</a> and presales organization so do not hesitate to drop him a note. He is also not sure if he should continue to talk about himself in the third person, but please let him be.
