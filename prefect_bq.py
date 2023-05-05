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

