#Функции взаимодействия с БД MySql
#выполняют подключение и загрузку данных в БД
import os
from datetime import  datetime

import numpy as np
from mysql.connector import connect, Error

from ParseConfig import parse_database_config
from Logger import create_logger
from CSVHandler import read_csv, split_col_names_data

#Подлючение к базе данных
def open_connection(user, password, database, host, port=3306):
    """
    Подключение к базе данных в MySQL
    """
    try:
        Logger.info("Подключение к базе данных " + database)
        connection = connect(user=user, password=password, database=database, host=host, port=port, buffered = True)
        return connection
    except Error:
        Logger.error("Ошибка подключения к базе данных " + database)
        return None

#Вставка валютных знаков в таблицу currency
#Поле currency_load_datetime заполняется с помощью вызова триггера before insert
def insert_currencies(connection, currency_names):
    """
    Вставка валютных знаков в БД    
    """
    try:
        Logger.info("Запись данных в таблицу currency")
        with connection.cursor() as cursor:
            query = "INSERT INTO currency (currency_id, currency_name) VALUES (%s, %s);"
            for currency_name in currency_names:
                cursor.execute(query, (None, currency_name))      
                connection.commit()
        Logger.info("Запись данных успешно завершена")
        return True
    except Error:
       Logger.info("Ошибка записи данных в таблицу currency. Ошибка: " + str(Error))
       return False

#Вставка значений курса валют из временного файла temp.csv
#Поле rate_load_datetime заполняется через триггер before insert 
def insert_rates(connection, data):
    """
    Вставка информации об изменении курса валют
    """
    #разбиваем матрицу на массив дат и массив курсов
    dates, rates = data[:, 0], data[:, 1:]
    try: 
        Logger.info("Начало записи данных в таблицу rate")
        with connection.cursor() as cursor:
            query = "INSERT INTO rate (rate_currency_id, rate_date, rate_value) VALUES (%s, %s, %s);"
            for i in range(len(dates)):
                key = 1
                for rate in rates[i, :]:
                    tp = (key,  datetime.strptime(dates[i], "%Y-%m-%d").date(), float(rate))
                    key += 1
                    cursor.execute(query, tp)
            connection.commit()
        Logger.info("Запись данных успешно завершена")
        return True
    except Error:
        Logger.error("Ошибка записи данных в таблицу rate")
        return False


Logger = create_logger("DBModel")
user, password, host, port, databases = parse_database_config()

connection = open_connection(user, password, databases["WareHouse"], host, port)


currency_names, _ = split_col_names_data(read_csv("temp/temp.csv"))

_, data = split_col_names_data( read_csv("temp/temp.csv"))
insert_rates(connection, data)