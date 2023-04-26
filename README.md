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
![image](https://user-images.githubusercontent.com/52333702/234568443-7d48ad76-95ef-4848-94bd-b0fb4651df3b.png)
![image](https://user-images.githubusercontent.com/52333702/234568502-d266c99a-9e2b-450f-adda-4e35e6f82733.png)
![image](https://user-images.githubusercontent.com/52333702/234568532-036c7164-c413-4b84-a59d-6f57216a546b.png)

# Summary
In this blog post, we explored how to automate data engineering tasks using Kaggle and Prefect. We demonstrated how to download CSV data from Kaggle and store it in Google Cloud Storage using Prefect. While Prefect provides a powerful workflow orchestration tool, it's essential to understand its pros and cons in a real-life work environment.
In the next blog we will show how to take data from Google Cloud Storage and transfer it to BigQuery, a powerful data warehousing solution offered by Google Cloud. By the end of the series, readers will have a comprehensive understanding of how to build an efficient and scalable data pipeline using Kaggle, Prefect, Google Cloud Storage, and BigQuery.
