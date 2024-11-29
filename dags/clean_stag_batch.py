from airflow import DAG
import json
import requests
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from airflow.models.xcom_arg import XComArg
from airflow.utils.task_group import TaskGroup
import logging

logging.basicConfig(level=logging.INFO)

# Define default args
default_args = {
    'owner': 'airflow',
    'retries': 1
}

# Load config file
dag_id = 'clean_stag_batch'
with open(f'/opt/airflow/configs/{dag_id}_config.json') as config_file:
    config = json.load(config_file)

# Initialize the DAG
with DAG(
    'clean_stag_batch',
    default_args=default_args,
    description='DAG to clean data in stag table in batches',
    schedule_interval=None,
) as dag:

    @task
    def get_data(batch_task):
        batch_size, offset = batch_task
        # Here we will download the data in batches and then clean it
        url = f"{config['api_path']}{config['get_endpoint']}?limit={batch_size}&offset={offset}"

        response = requests.get(url)
        data = response.json()

        # return to next task in the sequence
        return data

    @task
    def clean_data(batch_json):
        # This function is used to clean the data using pandas
        df = pd.read_json(batch_json)

        # Add the country column using last 5 chars of event name field
        df['Event Country'] = df['Event name'].apply(
            lambda x: x[-5:].strip().upper())
        return df.to_json()

    @task
    def save_to_new_table(cleaned_json):
        # Saves data to new cleaned table by calling save data API
        url = f"{config['api_path']}{config['save_endpoint']}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            url, json=json.loads(cleaned_json), headers=headers)
        return

    @task
    def create_batches(batch_size):
        # Get count of rows from the API
        url = f"{config['api_path']}{config['count_endpoint']}"
        response = requests.get(url)
        count = response.json()['total_records']
        logging.info(f'Count {count}')

        # Creating a set of tuples which will be used to get the data. (batch_size, offset). This will get data from db in batches
        batch_tasks = []
        for offset in range(0, count, batch_size):
            batch_tasks.append((batch_size, offset))

        logging.info(f'Created batches {batch_tasks}')

        return batch_tasks

    # Task flow. Dynamically create tasks
    batch_tasks = create_batches(config['batch_size'])
    batch_results = get_data.expand(batch_task=batch_tasks)
    cleaned_results = clean_data.expand(batch_json=batch_results)
    save_to_new_table.expand(cleaned_json=cleaned_results)
