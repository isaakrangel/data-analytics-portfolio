from airflow import DAG
from airflow.operators.bash import BashOperator


from datetime import datetime, timedelta

default_args = {
    "owner": "isaac",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="earthquake_weather_pipeline",
    default_args=default_args,
    description="Earthquake Risk Prediction Pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    end_date = datetime.today().strftime("%Y-%m-%d")

    # =====================================
    # Download Earthquakes
    # =====================================

    download_earthquakes = BashOperator(
        task_id="download_earthquakes",
        bash_command="""
        python /opt/airflow/project_data/scripts/AirFlow_download_earthquakes.py \
        --start_date {{ macros.ds_add(ds, -7) }} \
        --end_date {{ ds }}
        """
    )

    # =====================================
    # Create Weather Requests
    # =====================================

    create_weather_requests = BashOperator(
        task_id="create_weather_requests",
        bash_command="""
        python /opt/airflow/project_data/scripts/AirFlow_weather_requests.py
        """
    )

    # =====================================
    # Download Weather
    # =====================================

    download_weather = BashOperator(
        task_id="download_weather",
        bash_command="""
        python /opt/airflow/project_data/scripts/AirFlow_download_weather.py
        """
    )

    # =====================================
    # Merge Datasets
    # =====================================

    merge_datasets = BashOperator(
        task_id="merge_datasets",
        bash_command="""
        python /opt/airflow/project_data/scripts/AirFlow_merge_earthquake_weather.py \
        --earthquake_file $(ls /opt/airflow/project_data/data/raw/earthquakes_*.csv | tail -1 | xargs -n1 basename) \
        --weather_file $(ls /opt/airflow/project_data/data/processed/weather_*.csv | tail -1 | xargs -n1 basename)
        """
    )

    # =====================================
    # Data Cleaning
    # =====================================

    clean_dataset = BashOperator(
        task_id="clean_dataset",
        bash_command="""
        python /opt/airflow/project_data/scripts/Airflow_Data_Cleaning.py \
        --input_file $(ls /opt/airflow/project_data/data/processed/earthquakes_weather_merged.csv | xargs -n1 basename)
        """
    )

    (
        download_earthquakes >> create_weather_requests >> download_weather >> merge_datasets >> clean_dataset
    )