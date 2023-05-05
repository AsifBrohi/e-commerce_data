from google.cloud import bigquery
def query_bq(project_id :str,dataset :str,table_id :str) -> bigquery.QueryJob:
    client = bigquery.Client()
    full_table_id = f"{project_id}.{dataset}.{table_id}"
    job_config = bigquery.QueryJobConfig(destination=full_table_id)
    sql = """
        SELECT Warehouse_block
        FROM `dtc-de-ab.e_commerce_shipping_data.shipping_data`
        LIMIT 10;
    """
    query_job = client.query(sql, job_config=job_config)  # Make an API request.
    query_job.result()  # Wait for the job to complete.
    print(f"Query has been made for {dataset}.{table_id}")
    return query_job.result