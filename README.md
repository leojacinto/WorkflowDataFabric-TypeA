---
icon: magnifying-glass-chart
---

# Workflow Data Fabric Lab: Financial Intelligence at Scale

<figure><picture><source srcset=".gitbook/assets/wdf_connectors_banner_dark.gif" media="(prefers-color-scheme: dark)"><img src=".gitbook/assets/wdf_connectors_banner.gif" alt="Workflow Data Fabric"></picture><figcaption></figcaption></figure>

## Business motivation

Finance teams discover budget overruns weeks too late. Expense analysis requires manually piecing together data from ERP systems, data warehouses, and SharePoint. By the time finance reacts, small variances become major problems. **ServiceNow Workflow Data Fabric transforms reactive financial management into proactive intelligence**. By unifying data across systems through Zero Copy for SQL and ERP, Spokes, External Content Connectors, MCP, and AI agents, organizations can:

* **Detect budget issues in real-time** before they escalate
* **Scale financial operations** with AI agents, not headcount
* **Automate financial case creation** enriched with multiple external data sources and trend analysis

Your automations and AI Agents are just as good as your underlying data. Integrations powered by Workflow Data Fabric allow AI Agents to automate critical processes using accurate and consistent data.

With the trend of external agents reaching through enterprise data, it is worth examining why platform-native agents can scale more safely. Agents built within ServiceNow inherit battle-tested authorization models: role-based access, ACLs, and purpose-built security controls for AI agents; allowing organizations to automate confidently without stepping outside their governance boundaries.

## Persona context

You're a **Data Architect** serving the Finance department. Finance Managers need immediate visibility into budget performance. Cost Center Owners need to understand why they're over budget; with context beyond just numbers. **Your mission**: Build an intelligent financial data fabric that connects ServiceNow to external systems, deploys AI agents to detect and analyze budget issues automatically, surfaces executive guidance, and enables self-service analytics through Employee Center and Claude Desktop. You'll solve three critical problems:

1. "We find out about budget overruns too late: can we get real-time alerts?"
2. "Investigation means manually searching expenses, reports, and memos: can you unify this?"
3. "We answer the same questions daily: can employees self-serve?"

## Outcome

By completing this lab, you'll build an interconnected financial intelligence platform demonstrating:

* **Integration Hub** for real-time expense event processing
* **Zero Copy integration** with ERP and cloud warehouses (no data duplication)
* **MCP Server** enabling integration with any application that supports the protocol
* **AI agents** that autonomously searches via [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation), analyze trends, and create contextual cases
* **Lens and Document Intelligence** for invoice data capture individually or batch, respectively
* <mark style="color:$warning;">**\[Controlled Lab]**</mark>**&#x20;External Content Connector** bringing executive memos into making decisions
* **Finance Case Management** which receives the cases pre-processed by the AI Agents based on data taken from WDF

You'll master the architectural patterns for transforming siloed enterprise data into unified, intelligent decision-making platforms. **Let's build something intelligent**. 🚀💡

<figure><img src=".gitbook/assets/sc_readme_hero.png" alt=""><figcaption></figcaption></figure>

## Table of contents

This lab is divided into 5 exercises with the suggested sequence below. The ServiceNow-led lab environments which contains these exercises will allow you to complete individual labs in any sequence you prefer. The exercises focus on walk through and basic configuration of Workflow Data Fabric integrations and there are pre-made custom agents that make use of the integrations to demonstrate what is possible. You will not need to configure agents in this lab but steps are provided on how you can explore how the agents were configured.

This is designed to be a full day workshop covering most of WDF's capabilities. As such, we will not be able to cover in great depth all of the capabilities. If there are capabilities most relevant to your requirements, do ask your Lab Admin if there is a relevant deep dive lab available.

<table><thead><tr><th width="203.09375">Topic</th><th width="180.48828125">Difficulty</th><th>AI Agents involved</th><th>Suggested duration</th></tr></thead><tbody><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/data-and-flow-diagrams">Workflow Data Fabric Diagrams</a></td><td>N/A</td><td>No</td><td>N/A</td></tr><tr><td><strong>Main Exercises</strong></td><td></td><td></td><td></td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-fundamentals">Lab Exercise: Fundamentals</a></td><td>Basic</td><td>No</td><td>30 minutes</td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-integration-hub">Lab Exercise: Integration Hub</a></td><td>Intermediate</td><td>Yes</td><td>45 minutes</td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-zero-copy-connectors">Lab Exercise: Zero Copy Connectors</a></td><td>Intermediate</td><td>Yes</td><td>1 hour</td></tr><tr><td><strong>Extended Exercises</strong></td><td></td><td></td><td></td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-model-context-protocol-server-client">Lab Exercise: Model Context Protocol Server/Client</a></td><td>Intermediate</td><td>Yes</td><td>1 hour</td></tr><tr><td><a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-servicenow-lens-and-document-intelligence">Lab Exercise: ServiceNow Lens and Document Intelligence</a></td><td>Basic</td><td>Yes</td><td>30 minutes</td></tr><tr><td><strong>Hungry for more?</strong></td><td></td><td></td><td></td></tr><tr><td><mark style="background-color:$warning;"><strong>[Controlled Lab]</strong></mark> <a href="https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-external-content-connector">Lab Exercise: External Content Connector</a></td><td>Basic</td><td>Yes</td><td>20 minutes</td></tr></tbody></table>

## For Solution Consultants using internal Demo Hub

<mark style="background-color:$warning;">**\[Internal only]**</mark> There are steps in this lab which are different from the&#x20;

## Post-lab recommended materials

Below is a list of recommended courses that you can read up on after the lab to learn more about Workflow Data Fabric.

<table><thead><tr><th width="203.09375">Course</th><th width="180.48828125">Level</th><th>Type</th><th>Duration</th></tr></thead><tbody><tr><td><a href="https://learning.servicenow.com/lxp/en/automation-engine/suite-certification-workflow-data-fabric?id=learning_path_prev&#x26;path_id=668f6e1497069250e4fb72de2153af9d">Workflow Data Fabric</a></td><td>Advanced</td><td>Learning Path</td><td>4 days, 2 hours</td></tr><tr><td><a href="https://learning.servicenow.com/lxp/en/automation-engine/sprint-to-workflow-data-fabric-suite-certification?id=learning_course_prev&#x26;course_id=6862722387102e905aa9ca2d0ebb3591">Sprint to Workflow Data Fabric Suite Certification</a></td><td>Advanced</td><td>Course</td><td>2 days, 5 hours</td></tr></tbody></table>

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
* Use the provided screenshots and sample outputs as reference
* Adapt the exercises to your own data sources and systems

### Guided lab sessions and object dependencies

Fully provisioned environments with all dependencies pre-configured are available through ServiceNow-led workshops and enablement sessions. Please note that this lab uses the latest ServiceNow components as well as custom AI Agents and scoped objects, so provisioning requires lead time. Contact your ServiceNow representative or reach out to the author for availability.

### About the author

This lab is created by [Leo Francia](https://www.linkedin.com/in/leojmfrancia/), a Data Architect at ServiceNow, and is in no way a ServiceNow official manual. Leo is an active member of the [ServiceNow community](https://www.servicenow.com/community/workflow-data-fabric/ct-p/workflow-data-fabric) and presales organization so do not hesitate to drop him a note. He is also not sure if he should continue to talk about himself in the third person, but please let him be.

### Acknowledgement

This lab would not have been possible without the help of exceptional colleagues at ServiceNow:

* [Kamal Shewakramani](https://www.linkedin.com/in/kamal-shewakramani/)
* [Gurjot Joshi](https://www.linkedin.com/in/gurjotjoshi/)
* [Santosh Panda](https://www.linkedin.com/in/santosh-panda015/)
* [Jia Khee Lim](https://www.linkedin.com/in/jia-khee-lim-79427a151/)
* [Rahul Adlakha](https://www.linkedin.com/in/rahuladlakha/)
* [Theo Simmons](https://www.linkedin.com/in/theo-simmonsnow/)
* [Quentin Carton](https://www.linkedin.com/in/quentincarton/)
* [Dan Clark](https://www.linkedin.com/in/dannyclark/)
