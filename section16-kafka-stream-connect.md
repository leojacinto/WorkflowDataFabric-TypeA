# Section 16: Kafka Stream Connect Lab Guide

### Pre-requisites - Mandatory:
1. This lab is for ServiceNow internal only
2. Ensure you are able to HOP to hermes1 via this URL: http://hihop.service-now.com/hop.do?sysparm_instance=hermes1&mode=readwrite

### Pre-requisites - Recommended:
This will reduce effort in building the Kafka Producer:
1. Get a Docker account which can be created for free via https://www.docker.com/
2. Install Docker Desktop via https://docs.docker.com/desktop/
3. Open Docker, search for apache/kafka latest image by using the **Search** bar then click **Pull**
   <img src="screenshots/sc_docker_pull.png" height="400">

4. Go to **Images**, **Run** the Docker Image, accept defaults

   <img src="screenshots/sc_docker_run.png" height="400">

5. Go to Containers and see the newly created container with a randomized name; in the example below, it is vigilant_bartik and agitated_ardinghelli

   <img src="screenshots/sc_docker_image.png" height="400">

6. This will be the image you will use for Part X. Alternatively you can execute all of the steps in Part X in your local machine


### Part 1: Creating a data source
1. Go to All > search for **Data Sources**

<img src="screenshots/sc_data_source_start.png" height="300">

2. Click **New**

<img src="screenshots/sc_data_source_new.png" height="400">

3. Fill in the details for:
- a. Name, put in a descriptive name like **CMDB Data Array [Your Initials]**
- b. Import set table label, this will populate the **Import set table name**
- c. Type, select **File**
- d. Format, select **JSON**
- e. Put in **Path for each row** the characters **//**
- f. Tick **Data in single column**

  <img src="screenshots/sc_data_source_create.png" height="400">

- g. Right click on the header and click **Save**

  <img src="screenshots/sc_data_source_save.png" height="400">

4. Create a JSON file which has the structure of the data source. You can use the text below and save the file as **cmdb complex data array.json**
```
[{
    "table_name": "cmdb_ci_win_server",
    "site_code": "swmw1",
    "hostname" : "ktesthostname",
    "action": "ADD",
    "sys_class_name":"cmdb_ci_win_server",
    "data": 
    {
        "name": "K3 Complex Server",
        "site_code": "swmw1",
        "class": "Media",
        "entity_type": "media",
        "entity_subtype": "",
        "media_type": "",
        "location_a": "wynnarma",
        "location_z": "wynnarma",
        "last_unit": "00036",
        "first_unit": "00001",
        "mco": "",
        "number_wires": "2",
        "facility_detail": "lg-lgss",
        "sec": "sw1t0001",
        "media_designation": "rd010102"
    }              
}]
```
5. Upload the JSON file you just created
- a. Select the clip icon
- b. Click **Choose file** and upload the file from your machine
    <img src="screenshots/sc_data_source_json.png" height="400">

6. Right click on the header and click Save

    <img src="screenshots/sc_data_source_save.png" height="400">

7. Under Related Links click on **Test Load 20 Records**

    <img src="screenshots/sc_test_load.png" height="200">

### Part 2: Creating the transformation (ETL)
1. Go to All > search for IntegrationHub ETL

   <img src="screenshots/sc_ihub.png" height="300">
   
2. In IntegrationHub ETL home screen, click Create new

    <img src="screenshots/sc_ihub_create.png" height="400">
    
3. Under Specify Basic Details, click on Import Source Data and Provide Basic Details

   <img src="screenshots/sc_ihub_specify_basic.png" height="300">
   
4. Fill in the screen Provide Basic Information for the ETL Transform Map
- a. CMDB Application, select CMDB Import
- b. Name, put in a descriptive name like CMDB Complex Nested <Your Initials>
- c. Data Source, select the data source you created in Part 1
- d. Sample Import Set should populate automatically; if it does not, click on the magnifying glass and click the first item
- e. Preview Size Override, set to 100
- f. Click Save then Mark as Complete
  
    <img src="screenshots/sc_ihub_provide_basic.png" height="400">
    
5. Under Prepare Source Data for Mapping, click on Preview and Prepare Data

    <img src="screenshots/sc_ihub_prepare.png" height="300">

6. Fill in the screen Provide Basic Information for the ETL Transform Map
- a. Verify that when clicking on object in the first node of the tree on the left that your fields are similar to the screen here. Sequence is not important.
    <img src="screenshots/sc_ihub_preview_object.png" height="400">

- b. Verify that when click on in data in the third node on the tree to the left that your fields are similar to the screen here. This is a wide table so checking the first few fields is sufficient. Sequence is not important.
- c. Click Mark as Complete

    <img src="screenshots/sc_ihub_preview_data.png" height="400">

7. Under Map to CMDB and Add Relationships, click Select CMDB Classes to Map Source Data

    <img src="screenshots/sc_ihub_map_data_select.png" height="400">

8. Click in Add Conditional Class

    <img src="screenshots/sc_ihub_select_class.png" height="400">

10. A new dialog will pop-up
- a. Collection, select object
- b. Under If field, select object.table_name is cmdb_ci_linux_server
- c. Under Then Class field, select Linux Server
- d. Click New Criteria (not in screenshot)
- e. Under If field, select object.table_name is cmdb_ci_win_server
- f. Under Then Class field, select Windows Server
- g. Click Save

    <img src="screenshots/sc_ihub_add_class.png" height="400">

9. Set up mapping for Linux Server 1

    <img src="screenshots/sc_ihub_select_linux_mapping.png" height="400">
    
10. Fill up the details for Linux Server 1
- a. **Source Native Key** > **Source Column**, click on mapping button, type and select **hostname**

    <img src="screenshots/sc_ihub_select_linux_host.png" height="400">

- b. **Name** > **Source Column**, click on mapping button, type **data.name**, click on data then click on **name**

   <img src="screenshots/sc_ihub_select_linux_name.png" height="400">

- c. Using the same approach from the PREVIOUS screenshot, go to **Product instance identifier** > **Source Column**, click on mapping button, type **data.name**, click on data then click on **name**

- d. Using the same approach from the PREVIOUS screenshot, go to **Serial number** > **Source Column**, click on mapping button, type **data.site_code**, click on data then click on **site_code**
  
- e. The final output should be similar to below. Click back

   <img src="screenshots/sc_ihub_select_linux_final.png" height="400">
  
10. Set up mapping for Windows Server 1
- a. Source Native Key > Source Column, click on mapping button, type and select hostname
- b. Name > Source Column, click on mapping button, type data.name, click on data then click on name
- c. Product instance identifier > Source Column, click on mapping button, type data.name, click on data then click on name
- d. Serial number > Source Column, click on mapping button, type data.site_code, click on data then click on site_code
- e. Click Mark as Complete
- f. Click back
11. Click Mark as Complete to finish Select CMDB Classes to Map Source Data
12. Click Add Relationships
- a. Leave this blank this is jus to show the option to add Class Relationships if needed
- b. Click back
13. Under Preview Sample Integration Results and Schedule Import, Test and Rollback Integration Results
- a. Click Run Integration
- b. You should see  the results similar to below
- c. Click back then click Perform Rollback
14. Set up of ETL Transform Map is complete, click back

### Part 3: Setting up the consumer in Stream Connect





Instruction	Image
Navigate to Workflow Data Fabric Hub. If you had followed the setup instructions, your screen should look like the image. Click "Edit"

**Do not click "Test Connection"**

![Zcc](screenshots/zcc-1.png)


Click "Save and connect", then click "Continue" on the pop-up box. It should take about 30 seconds to load.	
You will be directed to the "Data assets" tab. These contain all the tables in the corresponding "catalog" in Databricks.

Click the "wdf_demo_now" folder	

![Zcc](screenshots/zcc-2.png)


We will use a sample dataset for POS transactions.
Click "pos_transaction_logs"
Data fabric tables tab should be empty as we have not created any data fabric tables yet.
Click "Columns", this will show you all the columns in the "pos_transaction_logs" table
Click "Create data fabric table"	


![Zcc](screenshots/zcc-3.png)


On "New data fabric table", enter Label: "Retail POS Transactions"
Name will be automatically generated
Click "Continue"

>Note that scope applies here, so you can create data fabric tables in scopes like how you would any custom table	
![Zcc](screenshots/zcc-4.png)

Click the select all check box as we want all the columns
Toggle true on primary for "transaction_id" - This will be our record identifier
Click "Finish", the "Confirm"	

![Zcc](screenshots/zcc-5.png)

Congratulations! You've successfully created a Data fabric table using ZCC with Databricks.
Click on the more icon next to your new data fabric table, then click "Open list"	

![Zcc](screenshots/zcc-6.png)

You will be brought to the list view of all records on the data fabric table. You can interact with this table like how you would on any other table in ServiceNow.	

![Zcc](screenshots/zcc-7.png)

## Part 2: Creating a subflow


Navigate to Workflow Studio
Click New > Subflow	

![Zcc](screenshots/zcc-8.png)

We will create the subflow from scratch. Click "Build on your own" tab.
Name the subflow: Lookup POS Transactions
Change Run as: "System user"
Click "Build subflow on your own"	

![Zcc](screenshots/zcc-9.png)

We will assume that the AI agent will want to query the last 4 digits of the card number, as well as the amount of the transaction
Create 2 inputs
Card number - string
Amount - string	

![Zcc](screenshots/zcc-10.png)

Create 2 outputs
Label: Card vendor, type: string
Label: Status of transaction, type: string	

![Zcc](screenshots/zcc-11.png)

Add a new action > Look Up Record
We are only returning for one record for simplicity

![Zcc](screenshots/zcc-12.png)

Table: Retail POS Transactions
Conditions: 
Amount is drag amount from input
AND
Card number contains drag Card number from input	

![Zcc](screenshots/zcc-13.png)

Add "Flow Logic" action > "Assign subflow outputs"
Add a new row to assign to "Card vendor" output with the "Card vendor" data pill from the look up record action
Do the same for "Status of transaction"

![Zcc](screenshots/zcc-14.png)
![Zcc](screenshots/zcc-15.png)

Let's test our Subflow.
First "Save" the subflow, then click "Test"
Enter Card number 7894, and Amount is 92.83	

![Zcc](screenshots/zcc-16.png)

View test results	

![Zcc](screenshots/zcc-17.png)


Go back and publish the flow	

![Zcc](screenshots/zcc-18.png)

## Part 3: Use in Agent

Create a new AI Agent
Use Now Assist: This agent retrieves POS transaction data.
Save and continue	

![Zcc](screenshots/zcc-19.png)
![Zcc](screenshots/zcc-20.png)

Add a tool: Subflow
Follow the inputs in the screenshot
Click Add
Save and continue
Hint: Remember to publish your subflow from before, if not the execution won't work in the next step	

![Zcc](screenshots/zcc-21.png)
![Zcc](screenshots/zcc-22.png)
![Zcc](screenshots/zcc-23.png)

Skip the next 2 pages for now to get to the testing page.

Your newly created AI agent should be selected. Enter the following task:
"help me find the information for a transaction that is 102.13, for a card number ending 7894"
Test	

![Zcc](screenshots/zcc-24.png)

Was it successful? What message did you get?	

![Zcc](screenshots/zcc-25.png)

Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Community
Docs
Contact
