---
hidden: true
---

# Lab Exercise: ServiceNow Document Intelligence and Lens

[Take me back to main page](./)

This lab will walk you through the configuration and usage of ServiceNow Lens and Document Intelligence as sources of unstructured document data for interactive and batch capture of expense information from documents.

**A note on this exercise:** In production, invoices are captured at the source: an ERP, procurement platform, or expense system, not uploaded directly into ServiceNow. ServiceNow's strength in this pattern is what happens _after_ ingestion: orchestrating validation against external data, enriching records via integration, and routing exceptions through case management. That's the capability we're demonstrating in most of the exercises in this lab.

To keep this exercise self-contained and reuse the agent built in [Lab Exercise: Integration Hub](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-integration-hub), we upload the document to a task record and let Document Intelligence extract it locally. Once the document is extracted, everything downstream such as the agent calls, the cross-system lookups, and the case creation, works the same regardless of how the document arrived. The document upload through a task table is a stand-in for the real action that happens in an ERP system. This exercise is about what ServiceNow _does_ with the document and is not about how it _receives_ it.

A more detailed version of this exercise with significantly more configuration steps is available as standalone. Reach out to your Lab Administrator for more details.

## Data flow

The data flow below shows how ServiceNow will get information from documents from invoices and further process said information to evaluate whether a Finance case should be created.

```mermaid
graph LR
    subgraph "User Interaction Layer"
        Employee((Employee/<br/>Finance Manager))
        EC[Employee Center or<br/>Workspace with Now Assist]
    end



    subgraph "AI Experiences"
        Lens["ServiceNow</br>Lens"]
        DocIntel["Document</br>Intelligence"]
    end

    subgraph "ServiceNow Workflow Data Fabric and related components"

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
            FinCase[(Finance Case<br/>Table)]
        end

        subgraph "AI & Automation"
            Agent1[Agent: Over-Budget<br/>Case Creator<br/>Zero Copy Source]
            Agent2[Agent: Proactive<br/>Budget Alert<br/>Integration Hub Source]
            RAG[RAG - Retrieval<br/>Augmented Generation]
            FlowAction[Flow Action]
        end
    end


    %% Data Flow Connections
    EC -->|Individual UI-based| Lens -->|Write| ExpenseTable
    EC -->|Individual UI-based| DocIntel -->|Write| ExpenseTable

    %% Agent 1 Workflow - Zero Copy Source
    ExpenseTable -->|Search Similar Cases| Agent1
    Agent1 -->|Create Case| FinCase
    Agent1 <-->|Trend Analysis| RAG
    Agent1 <-->|Flows/Subflows/Actions| FlowAction

    %% Agent 2 Workflow - Integration Hub Source
    ExpenseTable -->|Incoming Event| Agent2
    Agent2 -->|Create Case| FinCase

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

    class ERP,ExpenseAPI,SharePoint,CDW,MockERP,MockExpense external
    class ZeroCopySQL,ZeroCopyERP,IntHub,ExtContent integration
    class ExpenseTable,FinCase,FinVar native
    class Agent1,Agent2,RAG,NASK,FlowAction,MCP,GGraph,NLQuery,Lens,DocIntel ai
    class Employee,EC user
```

### Document Intelligence Configuration

1.  Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Now Assist Admin** > <mark style="color:green;">**b.)**</mark> click on **Now Assist Admin > Skills**.

    <figure><img src=".gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>
2.  Go to <mark style="color:green;">**a.)**</mark> **Platform** > <mark style="color:green;">**b.)**</mark>**&#x20;Other** > <mark style="color:green;">**c.)**</mark> type **Extract information from documents** > <mark style="color:green;">**d.)**</mark> click **Activate Skill**.

    <figure><img src=".gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>
3.  Go to <mark style="color:green;">**a.)**</mark> **Create Usecase** > <mark style="color:green;">**b.)**</mark> click on **Expense Transaction Event.**

    <figure><img src=".gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>
4. In this screen, you do not have to configure anything as this has been preconfigured as a custom **use case** under the standard platform skill **Extract information from documents**. The sub-steps below only serve as a tour of the different configuration components for a Document Intelligence components.&#x20;

<mark style="color:green;">**a.)**</mark>**&#x20;Status: Active** indicates that this has been activated prior.

<mark style="color:green;">**b.)**</mark>**&#x20;Target table: Expense Transaction Event** is the table that will save the extracted information from the documents. This can be a standard or a custom table

<mark style="color:green;">**c.)**</mark>**&#x20;Full automation mode: On** indicates that this skill will automatically process and extract the information from uploaded documents. If [Document Intelligence Admin](https://store.servicenow.com/sn_appstore_store.do#!/store/application/8700f4efc3a411101d9a3cadb140ddad/1.1.0) is installed, the thresholds fore **Full automation** to trigger can be set for each use case. Our scenario does not have it installed so we will configure the thresholds for Full automation mode in the latter steps.

<mark style="color:green;">**d.)**</mark>**&#x20;Field Names** show all of the relevant fields for this use case, these have been preconfigured.

<mark style="color:green;">**e.)**</mark>**&#x20;Target fields** show the fields from the **Target table** where the extracted information will be saved in.

<mark style="color:green;">**f.)**</mark>**&#x20;Type** is where the data type can be configured. For this scenario we are using Text for all as Document Intelligence is capable of mapping this to the appropriate data type in the target table in most cases.

<mark style="color:green;">**g.)**</mark> **Required** can be configured to set whether a field is mandatory for the Document Intelligence extraction, i.e. a blank required field will result into the extraction not being saved into the target table.

<mark style="color:green;">**h.)**</mark>**&#x20;+ New field** allows addition of new fields for Document Intelligence to extract. No additional fields are needed for this scenario.

<mark style="color:green;">**i.)**</mark>**&#x20;Settings (gear icon)** allow you to toggle **Full Automation mode** and **Manage LLMs**.

<mark style="color:green;">**j.)**</mark> Go to **Integrations** tab.

<figure><img src=".gitbook/assets/image (37).png" alt=""><figcaption></figcaption></figure>

5. In the integrations tab the following needs to be observed. The **Process** integration picks up the document from the source table and **Extract** integration extracts the contents of the document to be saved to the target table.

<mark style="color:green;">**a.)**</mark>**&#x20;Extract** integration should be present with the target table **x\_snc\_forecast\_v\_0\_expense\_transaction\_event (Expense Transaction Event)**.

<mark style="color:green;">**b.)**</mark>**&#x20;DocIntel Extract Values Flow - Expense Transaction Event - Extract** should be the Flow assigned. If it is not assigned, double click and type the name of the flow to assign it. This is a scoped Flow and is created specifically for this use case.

<mark style="color:green;">**c.)**</mark>**&#x20;Process** integration should be present with the target table **x\_snc\_forecast\_v\_0\_expense\_transaction\_event (Expense Transaction Event)**.

<mark style="color:green;">**d.)**</mark>**&#x20;DocIntel Task Processing Flow - Expense Transaction Event - Process** should be the Flow assigned. If it is not assigned, double click and type the name of the flow to assign it. This is a scoped Flow and is created specifically for this use case.

<mark style="color:green;">**e.)**</mark> If everything is correct, click **Exit**.

<figure><img src=".gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

6. Click **Save and Continue**.&#x20;

<figure><img src=".gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>

5.  Click **Activate**.&#x20;

    <figure><img src=".gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>
6.  Click **Return to Platform**.&#x20;

    <figure><img src=".gitbook/assets/image (25).png" alt="" width="563"><figcaption></figcaption></figure>
7.  You will be redirected to the Skills screen and this concludes the walkthrough of the Skills needed for document extraction.

    <figure><img src=".gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

### Document Intelligence Runtime

1. Steps 2 to 4 are applicable if you do **NOT** have [Document Intelligence Admin](https://store.servicenow.com/sn_appstore_store.do#!/store/application/8700f4efc3a411101d9a3cadb140ddad/1.1.0) plugin installed which is the case for this lab. Succeeding versions of this lab will have the said plugin installed which will result in a more streamlined experience.
2.  For this step, change the scope to Global by navigating to the <mark style="color:green;">**a.)**</mark> **globe icon** and clicking <mark style="color:green;">**b.)**</mark> **Global** application scope.

    <figure><img src=".gitbook/assets/image (30).png" alt="" width="321"><figcaption></figcaption></figure>
3. Navigate to All > <mark style="color:green;">**a.)**</mark> type **Document Data Extraction** > <mark style="color:green;">**b.)**</mark> click Document **Data Extraction > System Properties**.&#x20;

<figure><img src=".gitbook/assets/image (31).png" alt="" width="373"><figcaption></figcaption></figure>

4. Search for <mark style="color:green;">**a.)**</mark> **\*threshold** and update the values of the three parameters below <mark style="color:green;">**b.)**</mark> to **0.01**. This is to reduce the threshold for the automation and avoid trial and error issues. In a production environment, you are likely to test and fine-tune this to ensure exceptions are caught and corrected manually.

<figure><img src=".gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>

3. Change the scope to Global by navigating to the <mark style="color:green;">**a.)**</mark> **globe icon** and <mark style="color:green;">**b.)**</mark> searching and/or clicking **Forecast Variance** application scope.

<figure><img src=".gitbook/assets/image (33).png" alt="" width="319"><figcaption></figcaption></figure>

### Document Intelligence Runtime

1.  Go to **All** > type **x\_snc\_forecast\_v\_0\_variance\_task.do** and hit **Return/Enter ↵**.&#x20;

    <figure><img src=".gitbook/assets/image (45).png" alt=""><figcaption></figcaption></figure>
2. We will be uploading a document in the **x\_snc\_forecast\_v\_0\_variance\_task** task table. As mentioned earlier in this lab, ServiceNow is not a usual source of uploaded invoices as invoice uploads are normally done in ERP systems. The objective of these next steps is to show how ServiceNow would be able to capture information from similar documents and process them upstream. **Remember the automatically generated task ID!** Your task ID might differ from what is displayed in this screen, will need this later. Follow the steps below:

<figure><img src=".gitbook/assets/image (46).png" alt=""><figcaption></figcaption></figure>

<mark style="color:green;">**a.)**</mark> Put **CC\_IT\_002** as the short description. You can make it as descriptive as you like, the intent is to idenfify this as a document upload for this cost center.

<mark style="color:green;">**b.)**</mark> Click the **Attach (**[**paper clip**](https://cepr.org/voxeu/columns/ai-and-paperclip-problem)**)** button.

2. Obtain the invoice file to attach which is a sample invoice for CC\_IT\_002 cost center. File here: [**Invoice\_IT\_Laptop\_CC\_IT\_002.pdf**](https://raw.githubusercontent.com/leojacinto/WorkflowDataFabric-TypeA/refs/heads/main/.gitbook/assets/Invoice_IT_Laptop_CC_IT_002.pdf).
3.  Click **Choose file**.

    <figure><img src=".gitbook/assets/image (47).png" alt=""><figcaption></figcaption></figure>
4.  Upload the file > <mark style="color:green;">**a.)**</mark> [**Invoice\_IT\_Laptop\_CC\_IT\_002.pdf**](https://raw.githubusercontent.com/leojacinto/WorkflowDataFabric-TypeA/refs/heads/main/.gitbook/assets/Invoice_IT_Laptop_CC_IT_002.pdf) > <mark style="color:green;">**b.)**</mark> click **Exit (x)**.&#x20;

    <figure><img src=".gitbook/assets/image (48).png" alt=""><figcaption></figcaption></figure>
5.  Go to field > <mark style="color:green;">**a.)**</mark>**&#x20;State** and > <mark style="color:green;">**b.)**</mark> change it to **Work in Progress**.&#x20;

    <figure><img src=".gitbook/assets/image (49).png" alt=""><figcaption></figcaption></figure>
6.  You can _either_ <mark style="color:green;">**a.)**</mark> right-click on the header and click **Save** or > <mark style="color:green;">**b.)**</mark> simply click **Submit**.&#x20;

    <figure><img src=".gitbook/assets/image (50).png" alt=""><figcaption></figcaption></figure>
7.  In the same browser window, you will notice that there is a new **Now Assist badge**. This is the AI Agent at work in the back end because the Document Intelligence integration flows have been triggered by changing the status of the task in which we have uploaded the Invoice to. This in turn triggered the same agent in [Lab Exercise: Integration Hub](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-integration-hub). Click on the **Now Assist icon** with the updated badge count. If the **Now Assist badge** does not appear, simply reload your page.

    <figure><img src=".gitbook/assets/sc_ihub_now_assist_badge_notification.png" alt=""><figcaption></figcaption></figure>
8.  This will open the **Now Assist** chat. Click on the two-headed diagonal arrow to Enter **Modal**.

    <figure><img src=".gitbook/assets/sc_ihub_now_assist_chat_expand.png" alt=""><figcaption></figcaption></figure>
9. This will expand the Now Assist window.

<mark style="color:green;">**a.)**</mark> Expand **Planning the next steps** show tools used.

<mark style="color:green;">**b.)**</mark> Note the **Event ID** extracted from the invoice event. We are using **Event ID** to leverage the flow built in [Lab Exercise: Integration Hub](https://servicenow-lf.gitbook.io/the-workflow-data-fabric-loom/lab-exercise-integration-hub). Note that in a real business scenario, the relevant field would be invoice ID or something similar for such a document type used in this exercise.

<mark style="color:green;">**c.)**</mark> Note the **cost\_center** and **vendor** extracted from the expense event.

<mark style="color:green;">**d.)**</mark> There are no results from the **Retrieval-augmented Generation (RAG) search** for this vendor.

<mark style="color:green;">**e.)**</mark> You can also access the **RAG search** results for the vendors associated with the expense event.

<mark style="color:green;">**f.)**</mark> Finally, if the expense event will lead to the associated cost center being over budget, the total cost center expense and the **Finance Case** created for exceeding the budget for further review and action is listed. In this case it is FINC0010017.

<figure><img src=".gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

10. Navigate to Workspaces > <mark style="color:green;">**a.)**</mark> type **Finance Operations Workspace** and click on the <mark style="color:green;">**b.)**</mark> workspace with the same name.

<figure><img src=".gitbook/assets/sc_common_fow_nav.png" alt=""><figcaption></figcaption></figure>

11. For this exercise, we are not impersonating a persona so you remain as the System user.

<figure><img src=".gitbook/assets/sc_common_fow_system_user.png" alt=""><figcaption></figcaption></figure>

12. Go to <mark style="color:green;">**a.)**</mark> **list (list icon)** > <mark style="color:green;">**b.)**</mark> **Lists** > <mark style="color:green;">**c.)**</mark> sort by **Number** descending/ascending > <mark style="color:green;">**d.)**</mark> or look for the Finance case created by the AI Agent, FINC0010017 in the example above.&#x20;

    <figure><img src=".gitbook/assets/image (40).png" alt=""><figcaption></figcaption></figure>
13. Navigate to **All** > <mark style="color:green;">**a.)**</mark> type **Now Assist Admin** > <mark style="color:green;">**b.)**</mark> click on **Now Assist Admin > Skills**.

    <figure><img src=".gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>
14. Go to <mark style="color:green;">**a.)**</mark> **Platform** > <mark style="color:green;">**b.)**</mark>**&#x20;Other** > <mark style="color:green;">**c.)**</mark> type **Extract information from documents** > go to **Extract information from documents** > **vertical tree dot** > <mark style="color:green;">**d.)**</mark>**&#x20;Edit**.

    <figure><img src=".gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>
15. Go to <mark style="color:green;">**a.)**</mark> **Create Usecase** > <mark style="color:green;">**b.)**</mark> click on **Expense Transaction Event.**

    <figure><img src=".gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>
16. In the screen that follows, go to <mark style="color:green;">**a.)**</mark> **Test Outputs** > <mark style="color:green;">**b.)**</mark> note the **Task ID** automatically generated when you created an entry in **x\_snc\_forecast\_v\_0\_variance\_task**. Your task ID may differ from what is show here.  Finally, > <mark style="color:green;">**c.)**</mark> > click on **Process**.

    <figure><img src=".gitbook/assets/image (42).png" alt=""><figcaption></figcaption></figure>
17. You can do several things here. Notice the <mark style="color:green;">**a.)**</mark> **Invoice** you uploaded with the <mark style="color:green;">**b.)**</mark>**&#x20;information** now extracted. You can also see the <mark style="color:green;">**c.)**</mark>**&#x20;Status**. You also have the option to open the section into a new **Document Intelligence** window.

    <figure><img src=".gitbook/assets/image (43).png" alt=""><figcaption></figcaption></figure>
18. Congratulations! You have walked through the configuration and runtime of Document Intelligence, integrated with AI Agents that process the contents of the invoice for appropriate case handling for over-budget cost centers.

[Take me back to main page](./)
