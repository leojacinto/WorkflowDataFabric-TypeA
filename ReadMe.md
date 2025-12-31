# Workflow Data Fabric Lab: Financial Intelligence at Scale

### Dislcaimer
This lab requires you to have ServiceNow internal and external data services available to make the integration scenarios meaningful. If you wish to have this lab, its ServiceNow components, and its external service dependencies available for you, **a complete image with prerequisites and integrations will be externaly available for customers  soon**. If you have the components available for you to execute this in your environment, or simply want to get an idea how to execute the steps if you have a similar set-up, read on! This is designed to also provide a conceptual architecture of how ServiceNow alongside external systems can deliver end to end automation with Flows and/or AI Agents while allowing the user to access systems and AI however they prefer.

This lab is created by [Leo Francia](https://www.linkedin.com/in/leojmfrancia/), a Data Architect at ServiceNow, and is in no way a ServiceNow official manual. Leo is an active member of the [ServiceNow community](https://www.servicenow.com/community/workflow-data-fabric/ct-p/workflow-data-fabric) and presales organization so do not hesitate to drop him a note. He is also not sure if he should continue to talke about himself in the third person, but please let him be.

### Business Motivation
Finance teams discover budget overruns weeks too late. Expense analysis requires manually piecing together data from ERP systems, data warehouses, and SharePoint. By the time finance reacts, small variances become major problems.
**ServiceNow Workflow Data Fabric transforms reactive financial management into proactive intelligence**. By unifying data across systems through Zero Copy for SQL and ERP, Global Graph, and AI agents, organizations can:
* **Detect budget issues in real-time** before they escalate
* **Automate financial case creation** enriched with executive guidance and trend analysis
* **Enable self-service insights** through natural language queries in Employee Center
* **Scale financial operations** with AI agents, not headcount

### Persona Context
You're a **Data Architect** serving the Finance department. Finance Managers need immediate visibility into budget performance. Cost Center Owners need to understand why they're over budget; with context, not just numbers.
**Your mission**: Build an intelligent financial data fabric that connects ServiceNow to external systems, deploys AI agents to detect and analyze budget issues automatically, surfaces executive guidance, and enables self-service analytics through Employee Center and Claude Desktop.
You'll solve three critical problems:
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

You'll master the architectural patterns for transforming siloed enterprise data into unified, intelligent decision-making platforms.
**Let's build something intelligent**. 🚀💡

### Table of Contents
* [Workflow Data Fabric Diagrams](https://github.com/leojacinto/WorkflowDataFabric/blob/main/WDF_Diagrams.md)
* [Lab Exercise: Fundamentals](https://github.com/leojacinto/WorkflowDataFabric/blob/main/Fundamentals.md)
* [Lab Exercise: Zero Copy](https://github.com/leojacinto/WorkflowDataFabric/blob/main/Zero_Copy.md)
* [Lab Exercise: Integration Hub](https://github.com/leojacinto/WorkflowDataFabric/blob/main/Integration_Hub.md)
* [Lab Exercise: External Content Connector](https://github.com/leojacinto/WorkflowDataFabric/blob/main/External_Content_Connector.md)
* [Lab Exercise: Model Context Protocol Server/Client and AI Control Tower](https://github.com/leojacinto/WorkflowDataFabric/blob/main/MCP_and_AI_Control_Tower.md)
* [Lab Exercise: ServiceNow Lens and Document Intelligence](https://github.com/leojacinto/WorkflowDataFabric/blob/main/Lens_and_DocIntel.md)

 <img src="screenshots/sc_persona_wdf.png" height="400">
