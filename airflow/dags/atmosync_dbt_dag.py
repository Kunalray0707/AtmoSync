"""
AtmoSync Airflow dbt Transformation DAG
Triggers dbt build, run, and assertions on schedule.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'atmosync_analytics_team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    'atmosync_dbt_transformations',
    default_args=default_args,
    description='Triggers dbt models and schema data quality assertions',
    schedule_interval='0 * * * *',  # Every hour
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['atmosync', 'dbt', 'snowflake', 'marts'],
) as dag:

    dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command='cd /opt/dbt && dbt deps',
    )

    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command='cd /opt/dbt && dbt seed --target dev',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/dbt && dbt run --target dev',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/dbt && dbt test --target dev',
    )

    dbt_deps >> dbt_seed >> dbt_run >> dbt_test
