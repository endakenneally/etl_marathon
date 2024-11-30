import os
import json
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from sqlalchemy import create_engine, text
from airflow.operators.python import PythonOperator

# Define default args
default_args = {
    'owner': 'airflow',
    'retries': 1
}

# Intialize the DAG
dag = DAG(
    'create_tables',
    default_args=default_args,
    description='DAG to create Tables in Postgres Database',
    schedule_interval=None,
)

# Function to create tables in the database


def create_tables():
    # Database connection parameters
    postgres_conn_id = 'postgres_default'
    conn = BaseHook.get_connection(postgres_conn_id)

    dag_id = 'create_tables'
    with open(f'/opt/airflow/configs/{dag_id}_config.json') as config_file:
        config = json.load(config_file)

    sql_files = [f for f in os.listdir(
        config['sql_scripts_path'])if f.endswith(".sql")]
    if not sql_files:
        raise ValueError("No SQL files found in the directory!")

    # Connect to PostgsreSQL
    engine = create_engine(
        f'postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')

    with engine.connect() as connection:
        # Loop through SQL Files
        for sql_file in sorted(sql_files):
            file_path = os.path.join(config['sql_scripts_path'], sql_file)
            with open(file_path, "r") as file:
                sql = file.read()
                connection.execute(text(sql))
                print(f"Executed SQL file: {sql_file}")


# Define Task
create_tables_task = PythonOperator(
    task_id='create_tables_task',
    python_callable=create_tables,
    dag=dag
)
