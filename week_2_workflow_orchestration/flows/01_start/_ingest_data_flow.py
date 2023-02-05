import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(log_prints=True, tags=["extract"], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url: str):
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        #csv_name = 'yellow_tripdata_2021-01.csv.gz'
        csv_name = 'green_tripdata_2020-01.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f"wget {url} -O {csv_name}")

    #df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    #df = next(df_iter)

    df = pd.read_csv(csv_name)

    #df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    #df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    return df

@task(log_prints=True)
def transform_data(df):
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, retries=3)
def load_data(user, password, host, port, db, table_name, df):
    print(f"number of rows: {df.shape[0]}")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    df.to_sql(name=table_name, con=engine, if_exists='append')

@flow(name="Subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f"Logging Subflow for: {table_name}")

@flow(name="Ingest Data")
def main_flow(table_name: str = "yellow_taxi_trips"):
    user = "root"
    password = "root"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"

    #csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz"
    log_subflow(table_name)
    raw_data = extract_data(csv_url)
    
    #data = transform_data(raw_data)
    data = raw_data
    
    load_data(user, password, host, port, db, table_name, data)

if __name__ == '__main__':
    #main_flow(table_name = "yellow_taxi_trips")
    main_flow(table_name = "green_taxi_trips")