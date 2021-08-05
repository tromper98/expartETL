FROM puckel/docker-airflow
#Копирование скриптов в диркторию
COPY ./scripts /usr/local/scripts
#Копирование ExpartETL_DAG в директорию, где хранятся DAGи
COPY ExpartETL_DAG.py /usr/local/airflow/dags

COPY requirements.txt /usr/local/scripts

RUN pip install -r /usr/local/scripts/requirements.txt