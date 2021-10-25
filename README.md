### Slides covering DE tools as an alternative to Streamsets.

Created with [reveals.js](https://github.com/hakimel/reveal.js/)

Check out live version [here](https://santhoshkumar-kotteeswaran.github.io/data_pipline_presentation/index.html)

#### Navigating to Code:
```
code
|
|───airflow => Folder containing files realted to airflow
│       bs_dag.py => Airflow DAG code
│       requirements.txt => python dependencies  
|
|───dagster => Folder containing files realted to dagster
│       bs_dagster.py => Dagster DAG code
│       requirements.txt => python dependencies  

```


#### Pre-requisites:
1. [Docker](https://docs.docker.com/get-docker/)
2. [Docker Compose](https://docs.docker.com/compose/install/)
3. [PSQL Docker](https://dev.to/shree_j/how-to-install-and-run-psql-using-docker-41j2)
4. [Airflow Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
5. [Dagster](https://docs.dagster.io/getting-started)

#### Configurations:

1. PSQL: Run following inside PSQL container

```
create table bs (user_id string, item_id string);
insert into bs (user_id,item_id) values (it_1,it_2,it_3),(it_2,it_5,it_8);
```

2. Airflow:
    Configure following according to your PSQL and S3 in `code/airflow/bs_dag.py` 
    
    
    // PSQL DB
    * host
    * port
    * database
    * user
    * password

    
    //S3
    * aws_access_key_id
    * aws_secret_access_key

3. Dagster:
    Configure following according to your PSQL and S3 in `code/airflow/bs_dagster.py` 
    
    
    // PSQL DB
    * host
    * port
    * database
    * user
    * password

    //S3
    * aws_access_key_id
    * aws_secret_access_key

#### How to run project:
1. Airflow:
    1. Clone/Download this project
    2. Navigate to `code/airflow/`
    3. Move `bs_dag.py` to `/dags` (Folder structure you create as part of installing docker)
    4. Run `pip install -r requirements.txt`
    5. Navigate to localhost:8080

2. Dagster:
    1. Clone/Download this project
    2. Navigate to `code/dagster/`
    3. Run `pip install -r requirements.txt`
    4. Run `dagit -f bs_dagster.py`
    5. Navigate to localhost:3000


#### Documentation:
1. [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
2. [Dagster](https://docs.dagster.io/getting-started)

