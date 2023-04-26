from prefect import flow,task
import pandas as pd
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.bigquery import GcpCredentials
from pathlib import Path

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
    df = pd.read_csv(file_path)
    return df 

@task(log_prints=True)
def write_bq(df):
    df.to_gbq(
        destination_table = "e_commerce_shipping.shipping",
        project_id = "Dtc-de-ab",
        credentials = gcp_credentials_block.get_credentials_from_service_account(),
        if_exist = "append"
    )

@flow(name="elt to bq")
def elt_to_bigquery():
    data_path = 'dtc_data_lake_dtc-de-ab/../e-commerce_data/data/Train.csv'
    path_Gcs= extract_GCP(data_path)
    df = turn_into_df(path_Gcs)
    write_bq(df)

if __name__ == '__main__':
    elt_to_bigquery()