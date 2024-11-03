"""
Dag for ingestion & validation
using the taskflow API, KubernetesPodOperator and Dataset

"""

from datetime import timedelta
from os import getenv, path

# [START import_module]
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
# from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor, S3KeysUnchangedSensor
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from airflow.utils.dates import days_ago

# [END import_module]

DAGS_FOLDER_PATH = path.dirname(__file__)

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "GabrielPhilot",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["bilphilot@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 1,
    "retry_delay": timedelta(1),
}
# [END default_args]

# [START instantiate_dag]

# MUDAR NOME DEPOIS
dag = DAG(
    "ingestion-validation",
    default_args=default_args,
    schedule_interval="@once",
    tags=["spark", "kubernetes", "s3", "sensor", "minio", "bronze", "silver"],
)
# [END instantiate_dag]

# [START set_tasks]

start = DummyOperator(task_id='start', dag=dag)


ingestion = KubernetesPodOperator(
    task_id="tastk_ingestion_bronze_table",
    name="api-test-pod2",
    is_delete_operator_pod=True,
    namespace="orchestrator",
    pod_template_file=f"{DAGS_FOLDER_PATH}/python_jobs/testev0.yaml",
    kubernetes_conn_id="kubernetes_default",
    in_cluster=True,
    get_logs=True,
    do_xcom_push=True,
    dag=dag,
)


end = DummyOperator(task_id='end', dag=dag)
# [END set_tasks]
# [START task_sequence]
(
    start
    >> ingestion
    >> end
)
# [END task_sequence]
