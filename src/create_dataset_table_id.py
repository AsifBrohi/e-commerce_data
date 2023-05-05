from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from src.schema_bigquery import my_schema
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
    except KeyError as error:
        print(error)

def create_table_bq(data_set :str,table_id :str) -> bigquery.Table:
    """creating table in bigquery if does not exist"""
    client = bigquery.Client()
    full_table_id = f"{data_set}.{table_id}"
    
    try:
       existing_table = client.get_table(f"{data_set}.{table_id}")
       print(f"{existing_table} this table already exist")
       
    except NotFound:
        schema = my_schema
        table = bigquery.Table(full_table_id, schema=schema)
        table = client.create_table(table)
        print(f"Created table {full_table_id}")
        return table
    except ValueError as error:
        print(error)
