# Owner : Santhoshkumar Kotteeswaran
# Email : santhoshkumar.kotteeswaran@bigspark.dev

from dagster import pipeline, solid
import psycopg2
import pandas as pd
from io import StringIO
import boto3

# ----------------
# Solids
# ----------------

@solid
def db_connection():
    '''
    Description: Connect to postgres instance source data quality
    '''
    conn = psycopg2.connect(
    host="***",
    port="***",
    database="***",
    user="***",
    password="***")
    print("Connnection established")
    return conn

@solid
def source_quality_check(conn):
    '''
    Description: Checks source data quality 
    '''
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select count(*) from bs;")
    record = cur.fetchone()
    if (int(record[0])>1):
        print("Source check successful")  
    else:
        raise Exception('Source Check Failed') 

    return conn

@solid
def transform(conn):
    '''
    Description: Transforming source data
    '''
    conn = db_connection()
    sql = "select * from bs;"
    split_df = pd.read_sql_query(sql, conn)
    print (split_df)
    split_columns_input= ['item_id']    
    l=[]

    for i in split_columns_input:
        x=split_df[i].str.split(',', expand=True).stack().str.strip().reset_index(level=1,drop=True)
        l.append(x)

    split_intermediate_df = pd.concat(l, axis=1, keys=split_columns_input)
    split_df = split_df.drop(split_columns_input, axis=1).join(split_intermediate_df).reset_index(drop=True)
    return split_df

@solid
def load(context, split_df):
    '''
    Description: Load transformed data to S3
    '''
    bucket='santhosh2021bucket'
    csv_buffer = StringIO()
    split_df.to_csv(csv_buffer)

    s3_resource = boto3.resource('s3',
    aws_access_key_id='****',
    aws_secret_access_key= '****')

    s3_resource.Object(bucket, 'split_df.csv').put(Body=csv_buffer.getvalue())
    conn=None
    return None

# ----------------
# Pipeline
# ----------------

@pipeline
def bs_pipeline():
    load(
        transform(
        source_quality_check(
            db_connection()
            )
            )
        )

@daily_schedule(
    pipeline_name="bs_pipeline",
    start_date=datetime(2020, 10, 21),
    execution_time=time(12, 10),
    execution_timezone="US/Central",
)
def morning_schedule(date):
    return {
        "solids": {
            "db_connection": {},
            "source_quality_check":{},
            "transform":{}.
            "load":{}   
        }
    }

@repository
def hello_cereal_repository():
    return [bs_pipeline, morning_schedule]

# dagit -f bs_dagster.py -h 0.0.0.0 -p 3000