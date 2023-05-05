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

@flow(name = "CSV to GCS")
def main() -> None:
    """Main ELT function"""
    download_dir = "../e-commerce_data/data"
    extract_data(download_dir)
    path_data = f"{download_dir}/Train.csv"
    write_gcp(path_data)

if __name__ == "__main__":
    main()