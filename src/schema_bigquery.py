from google.cloud import bigquery
my_schema = [
            bigquery.SchemaField('Warehouse_ID', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Warehouse_block', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('Mode_of_Shipment', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('Customer_care_calls', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Customer_rating', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Cost_of_the_Product', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Prior_purchases', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Product_importance', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('Gender', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('Discount_offered', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Weight_in_gms', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('Reached_on_Time_Y_N', 'INTEGER', mode='REQUIRED'),        
            
        ]
