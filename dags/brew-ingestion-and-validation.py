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


# TODO DAG and task defaults

DAGS_FOLDER_PATH = path.dirname(__file__)

default_args = {
    "owner": "user",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

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

    # TODO define tasks ingestion
    @task_group(group_id='ingestion')
    def ingestion_group():
        @task
        def start_ingestion():
            print("Starting the ingestion part of the DAG")


        ingestion = KubernetesPodOperator(
            task_id="brewapi-ingestion-minio",
            name="brewapi-ingestion-minio",
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

    # TODO define tasks validation
    @task_group(group_id='validation')
    def validation_group():
        @task
        def start_validation():
            print("Starting the validation part of the DAG")

        validation = KubernetesPodOperator(
            task_id="brewapi-ingestion-validation-minio",
            name="brewapi-validation-minio",
            is_delete_operator_pod=True,
            namespace="orchestrator",
            pod_template_file=f"{DAGS_FOLDER_PATH}/python_jobs/brewapi_validation.yaml",
            kubernetes_conn_id="kubernetes_default",
            in_cluster=True,
            get_logs=True,
            do_xcom_push=True
        )

        @task(task_id="print_xcom_value")
        def print_xcom_value(**kwargs):
            # Recupera o contexto da tarefa
            ti = kwargs['ti']
            # Define o task_id da tarefa que gerou o XCom
            source_task_id = 'brewapi-ingestion-validation-minio'
            
            # Recupera o valor do XCom, incluindo execuções anteriores se necessário
            xcom_value = ti.xcom_pull(task_ids=source_task_id, include_prior_dates=True)
        
            # Exibe o valor do XCom, mesmo que seja zero
            if isinstance(xcom_value, dict) and "return_value" in xcom_value:
                return_value = xcom_value["return_value"]
                print(f"Valor do XCom da tarefa '{source_task_id}': {return_value}")
            else:
                print(f"Nenhum valor XCom válido encontrado para a tarefa '{source_task_id}'")

        @task
        def end_validation():
            print("Ending the validation part of the DAG")
        
        chain(
            start_validation(),
            validation,
            print_xcom_value(),
            end_validation()
        )

    ingestion = ingestion_group()
    validation = validation_group()

    ingestion >> validation
    
dag = brewapi_ingestion_validation_minio()