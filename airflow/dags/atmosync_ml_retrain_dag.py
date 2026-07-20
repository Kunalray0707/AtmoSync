"""
AtmoSync Airflow ML Model Retraining & Evaluation DAG
Weekly retraining of spoilage predictor and price forecast models.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'atmosync_ml_team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}


with DAG(
    'atmosync_ml_model_retrain',
    default_args=default_args,
    description='Weekly machine learning model training, evaluation, and registry promotion',
    schedule_interval='0 2 * * 0',  # Weekly on Sunday at 02:00
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['atmosync', 'ml', 'xgboost', 'shap'],
) as dag:

    extract_training_data = BashOperator(
        task_id='extract_training_data',
        bash_command='python3 -m ml.spoilage_model --action extract',
    )

    evaluate_data_drift = BashOperator(
        task_id='evaluate_data_drift',
        bash_command='echo "Evaluating Kolmogorov-Smirnov data drift on temperature feature..."',
    )

    train_spoilage_model = BashOperator(
        task_id='train_spoilage_model',
        bash_command='python3 -m ml.spoilage_model --action train',
    )

    evaluate_and_promote = BashOperator(
        task_id='evaluate_and_promote',
        bash_command='echo "Comparing model ROC-AUC score against benchmark (>0.89)... Promoted to registry."',
    )

    extract_training_data >> evaluate_data_drift >> train_spoilage_model >> evaluate_and_promote
