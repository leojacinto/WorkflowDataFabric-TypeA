---
icon: folder-grid
---

# Lab Exercise: External Content Connector

[Take me back to main page](../)

<mark style="color:$warning;">**Note:**</mark> This is a controlled lab and is only accessible in ServiceNow internal demo instances. Please bear with us as we translate this into a widely available lab exercise.

This lab will walk you through the configuration and usage of External Content Connectors as a source of unstructured document data to supplement automations needed in Finance case creation.

## Data flow

The data flow below shows how ServiceNow will get information from indexed documents from a document repository such as SharePoint to provide additional context and information to assist with Flows and Automations.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/> Workspace with Now Assist]
    end

    subgraph "External Systems"
        SharePoint[SharePoint<br/>Executive Memos]
    end

    subgraph "ServiceNow AI Platform"
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
    classDef external fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef user fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    classDef platform fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef wdf fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff

    class SharePoint external
    class ExtContent wdf
    class FinCase platform
    class Employee,EC user
```

> **Color Legend:** 🟢 Platform | 🟣 Workflow Data Fabric | 🔵 External Systems | 🔹 User Interaction

## Steps

### Crawl and Usage of External Content Connectors

This provides the steps to execute a crawl of documents to file repositories XCC (External Content Connectors) are set up for. This also provides the steps in a real life scenario on how XCC can help end users with their daily tasks.

This does not include steps in setting up XCC to connect to a SharePoint account as that requires SharePoint administrator rights which are not widely available to various personas.

1. Navigate to All > <mark style="color:green;">**a.)**</mark> type **External Content Connectors** > <mark style="color:green;">**b.)**</mark> click on **External Content Admin Home**.

<figure><img src="../.gitbook/assets/sc_xcc_xcc_home.png" alt=""><figcaption></figcaption></figure>

2. This will lead you the XCC home screen. Click on the pre-configured **SharePoint Online** connector. You can ignore the message **"Important Switch Scope to "External Content Connectors Admin" to create a connector."** This exercise will not require us to do that.

<figure><img src="../.gitbook/assets/sc_xcc_home_screen.png" alt="" width="563"><figcaption></figcaption></figure>

3. Navigate to <mark style="color:green;">**a.)**</mark> **Crawl History** > <mark style="color:green;">**b.)**</mark> click on **Crawl Content**.

<figure><img src="../.gitbook/assets/sc_xcc_crawl_content.png" alt=""><figcaption></figcaption></figure>

4. Click on <mark style="color:$success;">**a.)**</mark> **Full document crawl** > <mark style="color:$success;">**b.)**</mark>**&#x20;Create one-time crawl**.

<figure><img src="../.gitbook/assets/sc_xcc_one-time_crawl.png" alt="" width="563"><figcaption></figcaption></figure>

5. Select **Proceed**.

<figure><img src="../.gitbook/assets/sc_xcc_proceed.png" alt="" width="446"><figcaption></figcaption></figure>

6. Crawl job will be queued.

<figure><img src="../.gitbook/assets/sc_xcc_queue.png" alt="" width="563"><figcaption></figcaption></figure>

7. Wait for 5 to 10 minutes for the crawl job to finish. After the job has finished, it would have indexed the documents in SharePoint. In some cases, this can run up to 20+ minutes especially if there are a lot of large documents uploaded to SharePoint.

<figure><img src="../.gitbook/assets/sc_xcc_crawl_finished.png" alt="" width="563"><figcaption></figcaption></figure>

8. Click on <mark style="color:$success;">**a.)**</mark> **User profile** on top right corner (e.g., SA) > <mark style="color:$success;">**b.)**</mark>**&#x20;Impersonate user**.

<figure><img src="../.gitbook/assets/sc_xcc_impersonate.png" alt=""><figcaption></figcaption></figure>

9. In the pop-up that appears > <mark style="color:green;">**a.)**</mark> type the name of the XCC-mapped user **Chi Fen** > <mark style="color:green;">**b.)**</mark> click on **Chi Fen** in the drop down <mark style="color:green;">**c.)**</mark> then finally click on **Chi Fen** again to complete impersonation.

<figure><img src="../.gitbook/assets/sc_xcc_select_impersonation_chifen.png" alt="" width="446"><figcaption></figcaption></figure>

10. You will get an indication that the impersonation is successful if you see a red line on the top panel and if your user profile has changed and has a red line on the portrait image as well.

<figure><img src="../.gitbook/assets/sc_xcc_impersonation_successful.png" alt=""><figcaption></figcaption></figure>

11. Navigate to All > <mark style="color:green;">**a.)**</mark> type **Employee Center** > <mark style="color:green;">**b.)**</mark> click on **Employee Center**.

<figure><img src="../.gitbook/assets/sc_xcc_employee_center.png" alt=""><figcaption></figcaption></figure>

12. This will lead to the **Employee Center** home page. Click on **Now Assist** ("sparkle" icon) on the bottom right.

<figure><img src="../.gitbook/assets/sc_xcc_employee_center_home_page.png" alt="" width="563"><figcaption></figcaption></figure>

13. This will open a open a pop-up for **Now Assist**. Click on **Expand** (two-headed diagonal icon) on the top right so you can have a better typing workspace.

<figure><img src="../.gitbook/assets/sc_xcc_now_assist.png" alt="" width="311"><figcaption></figcaption></figure>

14. In the expanded pop-up, type: **Marketing team cost centre in France seems to have gone over-budget. Can you look for any documents that can assist in checking if there are management directives which might have triggered this?** Then hit **Return/Enter ↵**.

<figure><img src="../.gitbook/assets/sc_xcc_question.png" alt=""><figcaption></figcaption></figure>

15. You will get a <mark style="color:green;">**a.)**</mark> detailed response based on the SharePoint documents that were crawled earlier, which is also aligned with the over-budget entries. Click on the <mark style="color:green;">**b.)**</mark> number **1** then <mark style="color:green;">**c.)**</mark> click on the PDF file **Strategic Memo - European Product Launch.pdf**.

<figure><img src="../.gitbook/assets/sc_xcc_response_detail.png" alt=""><figcaption></figcaption></figure>

16. You will be directed to the file which has the content explaining why cost center **MKTG-FR-PR** went over-budget. You might be required to provide login/credentials, so if you are executing this lab in a ServiceNow managed environment, credentials to access this document will be provided separately in the lab session for security purposes.

<figure><img src="../.gitbook/assets/sc_xcc_overbudget.png" alt=""><figcaption></figcaption></figure>

## Conclusion

Congratulations! You have completed configuration of the **External Content Connector** integration that allows ServiceNow read indexed unstructured documents to supplement unstructured data for both interactive and AI Agent-based workflows.

## Next step

Keeping with the unstructured data theme, you can explore an exercise that focuses on how ServiceNow gets unstructured data from documents and feed them into ServiceNow forms or records.

[Take me back to main page](../)
