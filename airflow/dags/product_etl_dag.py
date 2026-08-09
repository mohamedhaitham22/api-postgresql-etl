from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.clients import APIClient
from src.database import engine
from src.extract import extract_products
from src.load import load_products
from src.storage import LocalStorage
from src.transform import transform_products


default_args = {
    "owner": "mohamed",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


# ==========================================================
# 1. Extract
# ==========================================================

def extract_task(**context):
    client = APIClient()

    try:
        products = extract_products(client)

        context["ti"].xcom_push(
            key="products",
            value=products,
        )

    finally:
        client.close()


# ==========================================================
# 2. Save Raw Data
# ==========================================================

def save_raw_task(**context):
    products = context["ti"].xcom_pull(
        task_ids="extract_products",
        key="products",
    )

    storage = LocalStorage()

    raw_file = storage.save_json(
        data=products,
        directory="products",
    )

    context["ti"].xcom_push(
        key="raw_file",
        value=str(raw_file),
    )


# ==========================================================
# 3. Transform
# ==========================================================

def transform_task(**context):
    products = context["ti"].xcom_pull(
        task_ids="extract_products",
        key="products",
    )

    transformed_data = transform_products(products)

    context["ti"].xcom_push(
        key="transformed_data",
        value=transformed_data,
    )


# ==========================================================
# 4. Load
# ==========================================================

def load_task(**context):
    transformed_data = context["ti"].xcom_pull(
        task_ids="transform_products",
        key="transformed_data",
    )

    load_products(
        engine=engine,
        transformed_data=transformed_data,
    )


# ==========================================================
# DAG
# ==========================================================

with DAG(
    dag_id="product_etl_pipeline",
    default_args=default_args,
    description=(
        "Extract products from API, save raw data, "
        "transform data, and load into PostgreSQL"
    ),
    start_date=datetime(2026, 8, 9),
    schedule="@daily",
    catchup=False,
    tags=["etl", "api", "postgresql", "products"],
) as dag:

    extract_products_task = PythonOperator(
        task_id="extract_products",
        python_callable=extract_task,
    )

    save_raw_data_task = PythonOperator(
        task_id="save_raw_data",
        python_callable=save_raw_task,
    )

    transform_products_task = PythonOperator(
        task_id="transform_products",
        python_callable=transform_task,
    )

    load_products_task = PythonOperator(
        task_id="load_products",
        python_callable=load_task,
    )

    extract_products_task >> save_raw_data_task
    save_raw_data_task >> transform_products_task
    transform_products_task >> load_products_task