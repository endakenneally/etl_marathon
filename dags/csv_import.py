from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.base_hook import BaseHook
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Define default_args
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 10),
    'retries': 1,
}

# Initialize the DAG
dag = DAG(
    'import_csv_to_postgres',
    default_args=default_args,
    description='A simple ETL DAG to import UM CSV data into Postgres',
    schedule_interval=None,
)

# Function to import CSV data to PostgreSQL


def import_csv_to_postgres():
    # Database connection parameters
    postgres_conn_id = 'postgres_default'
    conn = BaseHook.get_connection(postgres_conn_id)

    # CSV file path
    csv_file_path = "/opt/airflow/data/TWO_CENTURIES_OF_UM_RACES.csv"

    # Load the CSV data into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Connect to PostgreSQL
    engine = create_engine(
        f'postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')

    # Write the DataFrame to the table (create table if it does not exist)
    df.head(10000).to_sql('UM_DATA', con=engine,
                          index=False, if_exists='replace')


# Define the task to import the CSV into the database
import_csv_task = PythonOperator(
    task_id='import_csv_to_postgres_task',
    python_callable=import_csv_to_postgres,
    dag=dag,
)
