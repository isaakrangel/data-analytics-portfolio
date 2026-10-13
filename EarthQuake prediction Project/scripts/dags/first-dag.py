from datetime import datetime, timedelta
from airflow import DAG
#from airflow.operators.bash import BashOperator
#from airflow.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Python function to execute in task 2
def print_hello():
    print("Hola Mundo. From the Python script! Task 2 is running smoothly.")
    return "Python task completed"

# Define the DAG
with DAG(
    'simple_testing_dag',
    default_args=default_args,
    schedule='@daily',  # <--- CAMBIA 'schedule_interval' por 'schedule'
    catchup=False,
    tags=['testing'],
) as dag:

    # Task 1: Bash command
    task_start = BashOperator(
        task_id='start_test',
        bash_command='echo "Starting the pipeline test at $(date)"',
    )

    # Task 2: Python function execution
    task_process = PythonOperator(
        task_id='run_python_logic',
        python_callable=print_hello,
    )

    # Task 3: Final confirmation bash command
    task_end = BashOperator(
        task_id='end_test',
        bash_command='echo "Pipeline test finished successfully!"',
    )

    # Set the task dependencies (Pipeline Flow)
    task_start >> task_process >> task_end