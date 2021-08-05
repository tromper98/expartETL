#Создание DAG для Airflow
from typing import Dict, Any
import datetime as dt
from airflow.models import DAG, xcom
from airflow.operators.bash_operator import BashOperator

#Аргументы по умолчанию для DAG
args: Dict[str, Any]= {
    'owner': 'airflow',
    'start_date': dt.datetime(2021, 8, 4),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)

}

#Создание DAG
with DAG(dag_id="expartETL", default_args = args, schedule_interval='@daily') as dag:
    #Создание таска на запуск скрипта для загрузки данных с сайта
    load_currency = BashOperator(
        task_id="load_currency",
        bash_command="python /usr/local/scripts/DataLoader.py -o latest"
    )
    #Создание таска на запуск скрипта для вставки данных в бд
    insert_rates = BashOperator(
        task_id="insert_rates",
        bash_command="python /usr/local/scripts/DBModel.py -i rate"
    )
    #Создание таска на запуск скрипта для удаления временного файла
    remove_file = BashOperator(
        task_id="remove_expart_temp_file",
        bash_command="python /usr/local/scripts/CSVHandler.py -r temp"
    )
    #очередь тасков в DAG
    load_currency >> insert_rates >> remove_file
