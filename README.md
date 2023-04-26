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
``bash
pip install prefect 
pip install prefect_gcpt
``bash

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
