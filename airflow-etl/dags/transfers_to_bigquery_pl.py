from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.etl.bigquery import transfer_standings, transfer_top_scorers, transfer_fixtures, transfer_teams
from src.utils.constants import league_name_constants

default_args = {
    "owner" : "Ashish Wale",
    "retries" : 5,
    "retry_delay" : timedelta(minutes=2)
}

with DAG(
    dag_id="dag_transfers_to_gbq_pl",
    description="Orchestrates the daily data transfer of premier league into google big query.",
    start_date=datetime.now(),
    schedule_interval="@daily",
    default_args=default_args
) as dag:
    task_1 = PythonOperator(
        task_id="task_standings_to_gbq",
        python_callable=transfer_standings.start_pipeline,
        op_args=[league_name_constants.PREMIER_LEAGUE]
    )

    task_2 = PythonOperator(
        task_id="task_top_scorers_to_gbq",
        python_callable=transfer_top_scorers.start_pipeline,
        op_args=[league_name_constants.PREMIER_LEAGUE]
    )

    task_3 = PythonOperator(
        task_id="task_fixtures_to_gbq",
        python_callable=transfer_fixtures.start_pipeline,
        op_args=[league_name_constants.PREMIER_LEAGUE]
    )


    task_1, task_2, task_3