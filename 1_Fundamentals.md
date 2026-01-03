# Lab Exercise: Fundamentals

[Take me back to ReadMe](./)

This lab will walk you through creation of the scoped tables needed to interact with the external system integrations.

## Data flow

The data flow below shows how ServiceNow will consume REST API endpoints via Integration Hub Spokes then further processed by a Flow so the entries will be written in the scoped table.

```mermaid
graph LR
    subgraph "ServiceNow Workflow Data Fabric and related components"
        subgraph "Data Integration Layer"
            IntHub[Integration Hub<br/>Spoke/Flow]
        end

        subgraph "ServiceNow Native Tables"
            ExpenseTable[(Expense Event<br/>Line Items<br/>Scoped Table)]
        end
    end

    subgraph "External Systems"
        ExpenseAPI[Expense Event<br/>API]
    end

    %% Data Flow Connections
    ExpenseAPI -->|Real-time Events| IntHub
    IntHub -->|Write| ExpenseTable

    %% Styling
    classDef external fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef integration fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef native fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px

    class IntHub integration
    class ExpenseTable native
    class MockExpense external
```

## Lab story so far

While you have the power of CMDB at your fingertips, there are processes which require specific steps and data formats. You will need to create a scoped table which will store information from an expense event API.

## Steps

1. Go to the top right portion of your navigation and click on the <mark style="color:green;">**a.)**</mark> globe icon then the <mark style="color:green;">**b.)**</mark> list icon to change the scope.

<figure><img src=".gitbook/assets/sc_fund_scope_change.png" alt="" width="375"><figcaption></figcaption></figure>

2.  In the succeeding screen, click **New**.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_new_scope.png" alt="" width="360"><figcaption></figcaption></figure>
3.  Go to section **Start from Scratch** and click **Create**&#x20;

    <figure><img src=".gitbook/assets/sc_fund_create_scope.png" alt=""><figcaption></figcaption></figure>
4.  Provide the scope details with <mark style="color:green;">**a.)**</mark> name and the <mark style="color:green;">**b.)**</mark> scope. Click <mark style="color:green;">**c.)**</mark> Create. Note that the scope is a technical name and is automatically populated but you have the option to change it. In this example, the scope is **x\_snc\_forecast\_var**. Throughout the exercise, you will notice in screenshots that the scope name used is **x\_snc\_forecast\_v\_0**.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_scope_details.png" alt="" width="563"><figcaption></figcaption></figure>
5.  Verify that you are in the correct scope after you have created it. Being in the correct scope as you proceed with the lab will avoid scope access and object management issues. Do this by a.) clicking on the <mark style="color:green;">**a.)**</mark> scope (globe icon) and ensuring that has the value of the <mark style="color:green;">**b.)**</mark> Forecast Variance label you created.

    <figure><img src=".gitbook/assets/sc_fund_validate_scope.png" alt="" width="375"><figcaption></figcaption></figure>
6.  Now that you are in the right scope, you are ready to create the scoped table. Navigate to All > <mark style="color:green;">**a.)**</mark> type **System Definition** > <mark style="color:green;">**b.)**</mark> search for **Tables**&#x20;

    <figure><img src=".gitbook/assets/sc_fund_sysdef.png" alt="" width="375"><figcaption></figcaption></figure>
7.  Go to the top right section of the navigation and click **New**.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_new_table.png" alt="" width="563"><figcaption></figcaption></figure>
8.  Provide the <mark style="color:green;">**a.)**</mark> **Label** as **Expense Transaction Event**. The <mark style="color:green;">**b.)**</mark> **Name** which is a technical identifier will automatically be populated and can be modified to suit your requirement. Finally, untick <mark style="color:green;">**c.)**</mark> **Create module**.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_new_table_details.png" alt=""><figcaption></figcaption></figure>
9.  Right click on the header and click **Save**.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_save.png" alt="" width="135"><figcaption></figcaption></figure>
10. Staying in the same screen, an option to create fields for the table will be available. In the tab **Columns** click on **New**.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_new_field.png" alt=""><figcaption></figcaption></figure>
11. Let us use one column as an example. Provide the <mark style="color:green;">**a.)**</mark> **Type**, in this case **String**. Provide the <mark style="color:green;">**b.)**</mark> **Column label**, in this example, **Cost Center** which will automatically populate the <mark style="color:green;">**c.)**</mark> **Column name**. Since this is the string, provide the <mark style="color:green;">**d.)**</mark> **Max length** of **40**. Finally, right click on then header and <mark style="color:green;">**e.)**</mark> **Save**.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_field_details.png" alt="" width="563"><figcaption></figcaption></figure>
12. Do the same steps for all of the 16 other fields below. Note that the **Column label**, **Column name**, **Type**, **Max length** vary across some columns. For now, keep **Display** as **false** across all fields.&#x20;

    <figure><img src=".gitbook/assets/sc_fund_all_fields.png" alt=""><figcaption></figcaption></figure>

## Conclusion

Congratulations! You have created the destination table within ServiceNow for the external REST API sources.

## Next step

Let us continue building the data foundations for the use case. Next up is creation of the Data Fabric tables which will be used by AI Agents. Click [here to proceed with configuring the Data Fabric tables using ServiceNow's Zero Copy cpability](/broken/pages/qvtWnBJJ7yRVnf7LkGP6).

Alternatively, you can focus purely on REST API conectivity by proceeding with the [Integration Hub configuation](/broken/pages/Mxtr8y5z9iSBqS1mCbau).

[Take me back to ReadMe](./)
