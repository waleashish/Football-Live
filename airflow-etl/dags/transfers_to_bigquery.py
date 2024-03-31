from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.etl.bigquery import transfer_standings, transfer_top_scorers, transfer_fixtures

default_args = {
    "owner" : "Ashish Wale",
    "retries" : 5,
    "retry_delay" : timedelta(minutes=2)
}

with DAG(
    dag_id="dag_standings_to_gbq",
    description="Orchestrates the daily standings data of premier league teams into google big query.",
    start_date=datetime(2024, 3, 23, 0, 17),
    schedule_interval="@daily",
    default_args=default_args
) as dag:
    task1 = PythonOperator(
        task_id="task_standings_to_gbq",
        python_callable=transfer_standings.start_pipeline
    )

    task2 = PythonOperator(
        task_id="task_top_scorers_to_gbq",
        python_callable=transfer_top_scorers.start_pipeline
    )

    task_3 = PythonOperator(
        task_id="tak_fixtures_to_gbq",
        python_callable=transfer_fixtures.start_pipeline
    )

    [task1, task2, task_3]