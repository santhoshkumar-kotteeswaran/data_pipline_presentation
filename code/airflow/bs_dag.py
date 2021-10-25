# Owner : Santhoshkumar Kotteeswaran
# Email : santhoshkumar.kotteeswaran@bigspark.dev

from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import psycopg2
import pandas as pd
from io import StringIO
import boto3

# ----------------
# Python Operators
# ----------------

def db_connection():
    '''
    Description: Connect to postgres instance source data quality
    Inputs:
        host - machine IP
        port - machine port
        database - database name
        user - username
        password - password
    '''
    conn = psycopg2.connect(
    host="***",
    port="5432",
    database="***",
    user="****",
    password="***")
    return conn

def source_quality_check():
    '''
    Description: Checks source data quality 
    '''
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select count(*) from bs;")
    record = cur.fetchone()
    if (int(record[0])>1):
        print("Sucess")  
    else:
        raise Exception('Source Check Failed') 
    return None


def transform_load():
    '''
    Description: Transforming source data and load to S3
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
    print(split_df)
    bucket='santhosh2021bucket'
    csv_buffer = StringIO()
    split_df.to_csv(csv_buffer)

    s3_resource = boto3.resource('s3',
    aws_access_key_id='***',
    aws_secret_access_key= '***')

    s3_resource.Object(bucket, 'split_df.csv').put(Body=csv_buffer.getvalue())
    conn=None
    return None

# -----------------
# DAG Specification
# -----------------

default_args ={
    'owner':'airflow',
    'depends_on_past':False,
    'start_date':datetime(2019, 1, 12),
    'retires':0
}

dag = DAG(dag_id='bs_dag',default_args=default_args,catchup=False,schedule_interval='@once')

# -------------
# DAG operators
# -------------

start = DummyOperator(task_id='start',dag=dag)

source_quality_check = PythonOperator(
    task_id='source_quality_check', 
    python_callable=source_quality_check,
    dag=dag
)

transform_load = PythonOperator(
    task_id='transform_load', 
    python_callable=transform_load,
    dag=dag
)

end = DummyOperator(task_id='end', dag=dag)

# --------
# DAG Flow
# --------

start>>source_quality_check>>transform_load>>end