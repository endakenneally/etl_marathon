from airflow import DAG
import json
import requests
import pandas as pd


# Define default args
default_args = {
    'owner': 'airflow',
    'retries': 1
}

# Intialize the DAG
dag = DAG(
    'clean_stag_batch',
    default_args=default_args,
    description='DAG to clean data in stag table in batches',
    schedule_interval=None,
)


def get_data(batch_size, offset):
    # Here we will download the data in batches and then clean it
    dag_id = 'clean_stag_batch'
    with open(f'/opt/airflow/configs/{dag_id}_config.json') as config_file:
        config = json.load(config_file)

    url = f'{config['api_path']}{config['endpoint']}?limit={batch_size}&offset={offset}'
    response = requests.get(url)

    data = response.json()

    # return to next task in the sequence
    return data


def clean_data(batch_json):
    # This function is used to clean the data using pandas
    return


def save_to_new_table(cleaned_json):
    # Saves Data to new cleaned table

    return
