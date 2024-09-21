from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from aggregate_task import aggregate_data 
from datacleaner import data_cleaner

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 16),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}
today_date = datetime.strftime(datetime.now() , '%Y-%m-%d')

with  DAG(
        dag_id="store_raw_DAG_v6",
        schedule_interval="@daily",
        default_args=default_args,
        catchup=False,
        template_searchpath=['/usr/local/airflow/sql_files']
) as dag:
    t1 = FileSensor(
        task_id='check_file_exists',
        filepath='/usr/local/airflow/store_files_airflow/raw_store_transactions.csv',
    )

    t2 = PythonOperator(
        task_id='clean_raw_csv',
        python_callable=data_cleaner)

    t3 = MySqlOperator(
        task_id='create_mysql_table',
        mysql_conn_id="mysql_conn",
        sql="create_table.sql")

    t4 = MySqlOperator(
        task_id='insert_into_table',
        mysql_conn_id="mysql_conn",
        sql="insert_into_table.sql")

    t5 = PythonOperator(
        task_id='aggregate_task',
        python_callable=aggregate_data
    )

    t6 = BashOperator(task_id='move_file1',
                      bash_command='cat /usr/local/airflow/store_files_airflow/location_wise_profit.csv && mv /usr/local/airflow/store_files_airflow/location_wise_profit.csv /usr/local/airflow/store_files_airflow/location_wise_profit_%s.csv' % today_date
                      )

    t7 = BashOperator(task_id='move_file2',
                      bash_command='cat /usr/local/airflow/store_files_airflow/store_wise_profit.csv && mv /usr/local/airflow/store_files_airflow/store_wise_profit.csv /usr/local/airflow/store_files_airflow/store_wise_profit_%s.csv' % today_date
                      )

    t1 >> t2 >> t3 >> t4 >> t5 >> [t6, t7]