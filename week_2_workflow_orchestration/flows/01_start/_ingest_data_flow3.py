import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector

def parquet2csv(parquet_file, csv_file):
    df = pd.read_parquet(parquet_file, engine = 'pyarrow')
    df.to_csv(csv_file, index=False)


@task(log_prints=True, tags=["extract"], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url: str):

    parquet_file = 'output.parquet'
    csv_file = 'output.csv'
    os.system(f'wget {url} -O {parquet_file}')
    parquet2csv(parquet_file, csv_file)
    df = pd.read_csv(csv_file)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    return df

@task(log_prints=True)
def transform_data(df):
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, retries=3)
def load_data(table_name, df):
    print(f"number of rows: {df.shape[0]}")
    connection_block = SqlAlchemyConnector.load("postgres-connector2")
    with connection_block.get_connection(begin=False) as engine:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')


@flow(name="Subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f"Logging Subflow for: {table_name}")

@flow(name="Ingest Data")
def main_flow(table_name: str = "yellow_taxi_trips", prq_url: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2019-01.parquet"):
    log_subflow(table_name)
    data = extract_data(prq_url)
    load_data(table_name, data)

if __name__ == '__main__':
    main_flow(table_name = "yellow_taxi_trips_2019",
    prq_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2019-03.parquet"
    )