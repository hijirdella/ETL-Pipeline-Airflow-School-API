from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import requests

# Define default arguments
default_args = {
    'owner': 'hijir',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 5, 1)
}

# Function to fetch data from API
def fetch_data_from_api():
    response = requests.get('https://api-sekolah-indonesia.vercel.app/sekolah?page=1&perPage=5000')
    data = response.json()
    return data

# Function to transform data
def transform_data(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='fetch_data_from_api')
    # Extract the relevant data from the nested structure
    sekolah_data = data['dataSekolah']
    # Transform JSON data to DataFrame
    df = pd.DataFrame(sekolah_data)

    # Transformation 1
    # Filter and transform data using pandas
    transformed_df = df[(df['status'].str.contains('N')) & (df['bentuk'] == 'SMA')]

    # Transformation 2
    # Tambahkan kolom yang menggabungkan nama sekolah dan alamat jalan
    transformed_df['school_address'] = transformed_df['sekolah'] + " - " + transformed_df['alamat_jalan']

    # Transformation 3
    # Konversi kolom lintang dan bujur menjadi tipe data numerik
    transformed_df['lintang'] = pd.to_numeric(transformed_df['lintang'], errors='coerce')
    transformed_df['bujur'] = pd.to_numeric(transformed_df['bujur'], errors='coerce')

    # Transformation 4
    # Hapus baris dengan data lintang atau bujur yang kosong
    transformed_df = transformed_df.dropna(subset=['lintang', 'bujur'])

    return transformed_df

## Define Schema before load ( Change to your schema name)
custom_schema = 'hijir'

# Function to load data into database
# Define the custom schema name
def load_data_to_database(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(task_ids='transform_data')
    
    # Retrieve connection from Airflow
    postgres_hook = PostgresHook(postgres_conn_id='postgres')
    
    # Analyze data types of transformed data
    data_types = {col: 'TEXT' for col, dtype in transformed_data.dtypes.items()}
    
    # Create table if it doesn't exist
    create_query = f"""
    CREATE TABLE IF NOT EXISTS {custom_schema}.target_table (
        {', '.join([f'{col} {data_types[col]}' for col in transformed_data.columns])}
    );
    """
    postgres_hook.run(create_query)
    
    # Load data into the table with custom schema
    transformed_data.to_sql('target_table', postgres_hook.get_sqlalchemy_engine(), schema=custom_schema, if_exists='replace', index=False)


# Define the DAG
with DAG('api_to_database_dag_sekolah_hijir', default_args=default_args, start_date=datetime(2024, 5, 1), schedule_interval='@daily', catchup=False) as dag:
    
    extract_task = PythonOperator(
        task_id='fetch_data_from_api',
        python_callable=fetch_data_from_api
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True
    )
    
    load_task = PythonOperator(
        task_id='load_data_to_database',
        python_callable=load_data_to_database,
        provide_context=True
    )
    
    extract_task >> transform_task >> load_task