# Project Background 
In today's data-driven world, organizations generate and process vast amounts of data daily. Efficiently managing and processing this data is crucial for businesses to make informed decisions and gain insights. In this context, data engineering plays a significant role in ensuring data pipelines are scalable, reliable, and efficient.
In this blog post, we will explore how to use Kaggle and Prefect to download CSV data and store it in Google Cloud Storage (GCS) automatically. We will show how to set up a workflow that seamlessly extracts CSV data using Kaggle and uploads it to GCS using Prefect. The end goal is to provide a practical approach to automate data engineering tasks, allowing data engineers to focus on more significant data challenges.

# Dataflow, Work Orchestration & Prefect 
Dataflow defines all extraction and steps required for the data to be transferred from source to a destination ie Data Warehouse.
A workflow orchestration tool allows us to manage and visualize dataflows, while ensuring that they will be run according to a set of predefined rules.
## Introduction Of Prefect 
Prefect is a free and open-source platform that enables users to streamline their workflow orchestration and management tasks. Users can leverage Prefect to create and execute complex data pipelines that involve multiple steps, specify when they should be run, and automate their execution. It is primarily designed to run on cloud platforms like AWS and Google Cloud. Prefect offers built-in integrations with these platforms to make it easy to deploy and scale pipelines.
Moreover, Prefect also provides a graphical user interface (GUI) for visualizing and interacting with workflows
Overall, Prefect is a modern data engineering tool that aims to make the process of building, running, and maintaining data pipelines easy and efficient.

### How to pip install 
```python
pip install prefect 
pip install prefect_gcpt
```

# Extract Data 
```python
kaggle datasets download -d prachi13/customer-analytics --unzip -o -p {download_dir}
```
Turn this into a function with try and except blocks for error handling 
```python
import os 
def extract_data(download_dir: str) -> None:
    """extracting kaggle data set and downloading csv into local path"""
    file_path = os.path.exists(f"{download_dir}/Train.csv")
    try:
        if not file_path:
            os.system(f"kaggle datasets download -d prachi13/customer-analytics --unzip -o -p {download_dir}")
            print("Downloaded File")
        else:
            print("File Already exist")
    except FileNotFoundError as error:
        print(error)
        print("File not Found")
```
# Google Cloud Storage & Prefect_gcp blocks 
## Create a bucket
In the dtc-de-ab project, select Cloud Storage, and select Buckets. I already have a backup called dtc_data_lake_dtc-de-ab. 
Inside Orion, select Blocks at the left menu, choose the block GCS Bucket and click Add + button. Complete the form with:
Block Name: e-commerce-shipping-data
Name of the bucket: dtc_data_lake_dtc-de-ab

## Prefect Blocks
Blocks are a primitive within Prefect that enable the storage of configuration and provide an interface for interacting with external systems. With blocks, you can securely store credentials for authenticating with services like AWS, GitHub, Slack, and any other system you'd like to orchestrate with Prefect.
![image](https://user-images.githubusercontent.com/52333702/234567431-af10f0f2-f6f1-4468-8d03-4e2af43a22e4.png)


### Create service account
On Google Cloud Console, select IAM & Admin, and Service Accounts. Then click on + CREATE SERVICE ACCOUNT with these informations:
Service account details: zoom-de-service-account
Give the roles BigQuery Admin and Storage Admin.
![image](https://user-images.githubusercontent.com/52333702/234567551-e886a1cb-99fd-4b19-91cf-5ad06c2af6ac.png)

### Add the new key to the service account
Then, add a key on it. Click on ADD KEY + button, select CREATE A NEW KEY, select JSON and click on CREATE button.


### Adding Credentials 
When returning to the Orion form to create the GCS Bucket, which is called dtc_data_lake_dtc-de-ab, make sure the Gcp Credentials field says e-commerce-creds.

![image](https://user-images.githubusercontent.com/52333702/234567937-c78b8931-c47c-4ec2-8c39-d146544b1d5e.png)
![image](https://user-images.githubusercontent.com/52333702/234568118-e1b7640a-1d85-4475-91b1-f1010ba85c50.png)

We then obtain a fragment of code to insert into our python code. Which allows us to add the write_gcs method to prefect_storage.py.
![image](https://user-images.githubusercontent.com/52333702/234568298-10c5290a-5f17-4dc6-b3eb-196dcfb57515.png)


# ELT main script 
```python
from prefect import flow,task
import os
from prefect_gcp.cloud_storage import GcsBucket


@task(log_prints=True)
def extract_data(download_dir: str) -> None:
    """extracting kaggle data set and downloading csv into local path"""
    file_path = os.path.exists(f"{download_dir}/Train.csv")
    try:
        if not file_path:
            os.system(f"kaggle datasets download -d prachi13/customer-analytics --unzip -o -p {download_dir}")
            print("Downloaded File")
        else:
            print("File Already exist")
    except FileNotFoundError as error:
        print(error)
        print("File not Found")


 
@task(log_prints=True)
def write_gcp(path: str) -> None:
    """Upload CSV file into GCS"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("e-commerce-shipping-data")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path=f"{path}",
        to_path = path
    )
    return path

@flow(name = "Main run")
def main() -> None:
    """Main ELT function"""
    download_dir = "../e-commerce_data/data"
    extract_data(download_dir)
    path_data = f"{download_dir}/Train.csv"
    write_gcp(path_data)

if __name__ == "__main__":
    main()
```

We successfully transferred a CSV file into Cloud Storage using Prefect GCP. The task and flow were designed to transfer the file from a local directory to a Cloud Storage bucket. We utilized Prefect GCP's seamless integration with Google Cloud Storage to streamline the transfer process. The logs show that the task was completed successfully, with no errors or issues. The CSV file contains e-commerce shipping data, and its transfer to Cloud Storage will facilitate the use of BigQuerry. Overall, Prefect GCP proved to be an effective tool for this task, providing improved scheduling and monitoring capabilities, as well as easy integration with GCP services. The attached screenshots of the logs demonstrate the successful completion of the task seen below.

![image](https://user-images.githubusercontent.com/52333702/234568443-7d48ad76-95ef-4848-94bd-b0fb4651df3b.png)
![image](https://user-images.githubusercontent.com/52333702/234568502-d266c99a-9e2b-450f-adda-4e35e6f82733.png)
![image](https://user-images.githubusercontent.com/52333702/234568532-036c7164-c413-4b84-a59d-6f57216a546b.png)



# Extract CSV file from GCS
```python
def extract_GCP(path :str) -> None:
    gcs_path = f"{path}"
    gcs_block = GcsBucket.load("e-commerce-shipping-data")
    gcs_block.get_directory(
        from_path = gcs_path,
        local_path = f"../data/"
    )
    return Path(f"../{gcs_path}") 
```
This function takes a string parameter path which represents a file path in a Google Cloud Platform (GCP) bucket. It then uses the GcsBucket class to load a GCP bucket named "e-commerce-shipping-data" and fetches a directory from the specified path. The contents of the directory are downloaded to the local path "../data/". Finally, the function returns a Path object that points to the downloaded directory in the local file system.
Overall, this function appears to be designed to extract data from a GCP bucket and download it to the local file system for further processing.

# Transform Data
```python 
def turn_into_df(file_path :str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as error:
        print(error)
        print("File Does not Exist")

def transform_data(df :pd.DataFrame) -> pd.DataFrame:
    """cleaning up column name as Bigquery will not allow to load"""
    try:
        transform_df =df.rename(columns={"Reached.on.Time_Y.N":"Reached_on_Time_Y_N","ID":"Warehouse_ID"})
        return transform_df
    except pd.DataFrame.empty as error_empty:
        print(error_empty)
        print("Dataframe was not transformed")
```
# Create Dataset_id and Table_id Using BigQuery API on python 
I used the Google Cloud documentation to create functions for creating datasets and tables. These functions include a try-except block to catch errors, as well as checks to ensure that the dataset and table do not already exist before creating new ones. This helps to prevent any duplicate entries and streamlines the process of working with Google Cloud
```python 
def create_dataset_bq(dataset_id :str)->bigquery.Dataset:
    """creating a dataset within bigquery if does not exist"""
    client = bigquery.Client()
    full_dataset_id = f"{client.project}.{dataset_id}"
    dataset = bigquery.Dataset(full_dataset_id)
   
    try:
        existing_datset = client.get_dataset(dataset_id)
        print(f"{existing_datset} this dataset already exist")
    except NotFound:
            dataset.location = 'EU'
            dataset = client.create_dataset(dataset)  # Make an API request.
            print(f"Created dataset {client.project}.{dataset.dataset_id}")
    return dataset

def create_table_bq(data_set :str,table_id :str) -> bigquery.Table:
    """creating table in bigquery if does not exist"""
    client = bigquery.Client()
    full_table_id = f"{data_set}.{table_id}"
    
    try:
       existing_table = client.get_table(f"{data_set}.{table_id}")
       print(f"{existing_table} this table already exist")
```
# Load Dataframe into BigQuery

```python
def write_bq(df :pd.DataFrame,dataset_name :str)-> None:
    gcp_credentials_block = GcpCredentials.load("e-commerce-creds")
    df.to_gbq(
        destination_table = dataset_name,
        project_id = "dtc-de-ab",
        credentials = gcp_credentials_block.get_credentials_from_service_account(),
        if_exists = "append",
    )
```
# Prefect task and flow full script 
```python 
from prefect import flow,task
import pandas as pd
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.bigquery import GcpCredentials
from pathlib import Path
from src.create_dataset_table_id import create_dataset_bq
from src.create_dataset_table_id import create_table_bq

@task(log_prints=True)
def extract_GCP(path :str) -> None:
    gcs_path = f"{path}"
    gcs_block = GcsBucket.load("e-commerce-shipping-data")
    gcs_block.get_directory(
        from_path = gcs_path,
        local_path = f"../data/"
    )
    return Path(f"../{gcs_path}")

@task(log_prints=True)
def turn_into_df(file_path :str) -> pd.DataFrame:
    """turning filepath into a Dataframe"""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as error:
        print(error)
        print("File Does not Exist")

@task(log_prints=True)
def transform_data(df :pd.DataFrame) -> pd.DataFrame:
    """cleaning up column name as Bigquery will not allow to load"""
    try:
        transform_df =df.rename(columns={"Reached.on.Time_Y.N":"Reached_on_Time_Y_N","ID":"Warehouse_ID"})
        return transform_df
    except pd.DataFrame.empty as error_empty:
        print(error_empty)
        print("Dataframe was not transformed")

@task(log_prints=True)
def write_bq(df :pd.DataFrame,dataset_name :str)-> None:
    """load data to bigquery"""
    gcp_credentials_block = GcpCredentials.load("e-commerce-creds")
    df.to_gbq(
        destination_table = dataset_name,
        project_id = "dtc-de-ab",
        credentials = gcp_credentials_block.get_credentials_from_service_account(),
        if_exists = "append",
    )

@flow(name="elt to bq")
def elt_to_bigquery()-> None:
    data_path = 'dtc_data_lake_dtc-de-ab/../e-commerce_data/data/Train.csv'
    path_Gcs= extract_GCP(data_path)
    df = turn_into_df(path_Gcs)
    clean_df = transform_data(df)
    dataset_id = "e_commerce_shipping_data"
    dataset = "dtc-de-ab.e_commerce_shipping_data"
    table_id = "shipping_data"
    dataset_name = "e_commerce_shipping_data.shipping_data"
    create_dataset_bq(dataset_id)
    create_table_bq(dataset,table_id)
    write_bq(clean_df,dataset_name)

if __name__ == '__main__':
    elt_to_bigquery()
```
The task and flow were desinged to extract csv data from google cloud storage bucket. The CSV file was e-commerce shipping data and was extracted from kaggle dataset seen in my previous blog. Created a function which saves the CSV file into my local directory this function and what it does can be seen in the "extract CSV file from google cloud storage" heading of this blog . Turn it into a Dataframe to make transformations such as renaming columns in the Dataframe being Reached.on.Time_y.N as BigQuery does not allow "." within the coulmn name and changed ID to a more specfic and understandaing column name Warehouse_ID. Using gbq loaded the data into BigQuery Database. 
Through the use of Google Cloud Storage, custom functions, and the powerful BigQuery database, I was able to accomplish this task and generate logs and flow diagrams in Prefect to confirm its successful completion seen below.






# Summary
In this blog post, we explored how to automate data engineering tasks using Kaggle and Prefect. We demonstrated how to download CSV data from Kaggle and store it in Google Cloud Storage using Prefect. While Prefect provides a powerful workflow orchestration tool, it's essential to understand its pros and cons in a real-life work environment.
In the next blog we will show how to take data from Google Cloud Storage and transfer it to BigQuery, a powerful data warehousing solution offered by Google Cloud. By the end of the series, readers will have a comprehensive understanding of how to build an efficient and scalable data pipeline using Kaggle, Prefect, Google Cloud Storage, and BigQuery.
