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
    classDef user fill:#F5F5F5,stroke:#616161,stroke-width:3px,color:#1a1a1a
    classDef platform fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef wdf fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff

    class SharePoint external
    class ExtContent wdf
    class FinCase platform
    class Employee,EC user
```

> **Color Legend:** 🟢 Platform | 🟣 Workflow Data Fabric | 🔵 External Systems | ⚪ User Interaction

## Steps

### Preparation steps

1.  Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Users and Groups** > <mark style="color:green;">**b.)**</mark> click on **Users and Groups > Users**.

    <figure><img src="../.gitbook/assets/sc_common_agent_studio_users_nav.png" alt=""><figcaption></figcaption></figure>
2.  Search for <mark style="color:green;">**a.)**</mark> **System Administrator** then hit **Return/Enter ↵** > <mark style="color:green;">**b.)**</mark> click on **admin**.

    <figure><img src="../.gitbook/assets/sc_common_search_admin_user.png" alt=""><figcaption></figcaption></figure>
3.  Set the <mark style="color:green;">**a.)**</mark> **Email** to **demouser@wdfdemo.onmicrosoft.com**, <mark style="color:green;">**b.)**</mark> click **Save**. Then <mark style="color:green;">**c.)**</mark> click **Roles** then <mark style="color:green;">**d.)**</mark> click **Edit**.

    <figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>
4.  Search for <mark style="color:green;">**a.)**</mark> **ais\_high\_security\_admin** > <mark style="color:green;">**b.)**</mark> click on **ais\_high\_security\_admin** > <mark style="color:green;">**c.)**</mark> click on **>** to move the role to the right panel > then <mark style="color:green;">**c.)**</mark> click **Save**.&#x20;

    <figure><img src="../.gitbook/assets/image (1).png" alt="" width="563"><figcaption></figcaption></figure>
5.  Right-click on the top panel and click **Save**.

    <figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>
6.  <mark style="color:red;">**IMPORTANT**</mark>. Log out and log back in. Click on&#x20;

    <figure><img src="../.gitbook/assets/sc_common_logout.png" alt="" width="254"><figcaption></figcaption></figure>

### Crawl and Usage of External Content Connectors

This provides the steps to execute a crawl of documents to file repositories XCC (External Content Connectors) are set up for. This also provides the steps in a real life scenario on how XCC can help end users with their daily tasks.

This does not include steps in setting up XCC to connect to a SharePoint account as that requires SharePoint administrator rights which are not widely available to various personas.

1.  For this step, change the scope to Global by navigating to the <mark style="color:green;">**a.)**</mark> **globe icon** and clicking <mark style="color:green;">**b.)**</mark> **Global** application scope.

    <figure><img src="../.gitbook/assets/sc_ldi_scope_global.png" alt="" width="321"><figcaption></figcaption></figure>
2.  Elevate your role. Click on&#x20;

    <figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>
3.  Choose the role to elevate.

    <figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>
4. Navigate to All > <mark style="color:green;">**a.)**</mark> type **External Content Connectors** > <mark style="color:green;">**b.)**</mark> click on **External Content Admin Home**.

<figure><img src="../.gitbook/assets/sc_xcc_xcc_home.png" alt=""><figcaption></figcaption></figure>

2.  This will lead you the XCC home screen. Click on **Create** to create a new connection.

    <figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>
3.  You will be asked to select a source. Depending on your instance image, you may have multiple options. For this exercise, you only need **SharePoint**. <mark style="color:green;">**a.)**</mark> Select it and <mark style="color:green;">**b.)**</mark> click **Next**.

    <figure><img src="../.gitbook/assets/image (14).png" alt="" width="563"><figcaption></figcaption></figure>
4. Input the following details in the next screen. As some of r

<mark style="color:green;">**a.)**</mark> **Connector Name: SharePoint Online \<YOUR INITIALS>**

<mark style="color:green;">**b.)**</mark> **Application (client) ID: 26ec3997-e7da-4a95-91dd-d19f8c66b849**

<mark style="color:green;">**c.)**</mark> **Directory (tenant) ID: 53136633-b712-40ba-8c0b-0747745c05be**

<mark style="color:green;">**d.)**</mark> **JKS Certificate:** [obtain here](https://servicenow.sharepoint.com/:u:/s/iaapj/IQC6aY0kjVdSQYrYR8JkpYi3AUVOyZAxfP3GsT6W96xpWII?e=Ee7nZt) and upload, <mark style="color:$warning;">**ServiceNow internal login required**</mark>

<mark style="color:green;">**e.)**</mark> **JKS certificate password:** [obtain here](https://servicenow.sharepoint.com/:x:/s/iaapj/IQA9-mRIzGQYSaI0ab6a--VYAQv5ZKgUGg0RVyiTdEDezq4?e=1gXVAa) <mark style="color:$warning;">**ServiceNow internal login required**</mark>

<mark style="color:green;">**f.)**</mark> **JKS certificate thumbprint:** [obtain here](https://servicenow.sharepoint.com/:x:/s/iaapj/IQA9-mRIzGQYSaI0ab6a--VYAQv5ZKgUGg0RVyiTdEDezq4?e=1gXVAa), <mark style="color:$warning;">**ServiceNow internal login required**</mark>

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

5. Click Next.

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

5. Click Next.

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

6.  Click Next.&#x20;

    <figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>
7.  Click Next. <mark style="color:red;">**\[Update to include user permission crawl]**</mark>

    <figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>
8.  Proceed.

    <figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>
9.  Save.

    <figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>
10. Completed.

    <figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>
11. Click on <mark style="color:green;">**a.)**</mark> **User profile** on top right corner (e.g., SA) > <mark style="color:green;">**b.)**</mark>**&#x20;Impersonate user**.

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
