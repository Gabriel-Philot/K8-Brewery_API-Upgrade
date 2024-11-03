"""
Dag for ingestion & validation
using the taskflow API, KubernetesPodOperator and Dataset

"""

# TODO define libraries and imports
from airflow import Dataset
from airflow.decorators import dag, task, task_group
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import chain
from datetime import datetime, timedelta
from os import path
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)


DAGS_FOLDER_PATH = path.dirname(__file__)

# TODO DAG and task defaults
default_args = {
    "owner": "user",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}



# TODO DAG and task defaults
@dag(
    dag_id="brewapi-ingestion-validation-minio",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["spark", "kubernetes", "s3", "sensor", "minio", "bronze", "silver"],
)


# [START set_tasks]


def brewapi_ingestion_validation_minio():
    """Main DAG for Berewery ingestion and validation"""

    @task_group(group_id='ingestion')
    def ingestion_group():
        @task
        def start_ingestion():
            print("Starting the ingestion part of the DAG")


        ingestion = KubernetesPodOperator(
            task_id="brewapi-ingestion-minio",
            name="api-test-pod2",
            is_delete_operator_pod=True,
            namespace="orchestrator",
            pod_template_file=f"{DAGS_FOLDER_PATH}/python_jobs/brewapi_ingestion.yaml",
            kubernetes_conn_id="kubernetes_default",
            in_cluster=True,
            get_logs=True,
            do_xcom_push=True
        )


        @task
        def end_ingestion():
            print("Ending the ingestion part of the DAG")

        chain(
            start_ingestion(),
            ingestion,
            end_ingestion()
        )

    @task_group(group_id='validation')
    def validation_group():
        @task
        def start_validation():
            print("Starting the validation part of the DAG")

        @task
        def end_validation():
            print("Ending the validation part of the DAG")
        
        chain(
            start_validation(),
            end_validation()
        )

    ingestion = ingestion_group()
    validation = validation_group()

    ingestion >> validation
    
dag = brewapi_ingestion_validation_minio()