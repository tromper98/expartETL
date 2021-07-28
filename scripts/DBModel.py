#Функции взаимодействия с БД MySql
#выполняют подключение и загрузку данных в БД
import argparse
from datetime import  datetime
import traceback

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
        Logger.error("Ошибка подключения к базе данных " + database,  traceback.format_exc())
        return None

#Вставка валютных знаков в таблицу currency
#Поле currency_load_datetime заполняется с помощью вызова триггера before insert
def insert_currencies(connection, currency_codes):
    """
    Вставка валютных знаков в БД    
    """
    try:
        Logger.info("Запись данных в таблицу currency")
        with connection.cursor() as cursor:
            query = "INSERT INTO currency (currency_id, currency_name) VALUES (%s, %s);"
            for currency_code in currency_codes:
                cursor.execute(query, (None, currency_code))      
                connection.commit()
        Logger.info("Запись данных успешно завершена")
    except Error:
       Logger.error("Ошибка записи данных в таблицу currency. Ошибка: ",  traceback.format_exc())

#Вставка значений курса валют из временного файла temp.csv
#Поле rate_load_datetime заполняется через триггер before insert 
def insert_rates(connection, data):
    """
    Вставка информации об изменении курса валют
    """
    #разбиваем матрицу на массив дат и массив курсов
    data = np.array(data)
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
    except Error:
        Logger.error("Ошибка записи данных в таблицу rate",  traceback.format_exc())

#Вставка названий валют на русском и английском языках
def insert_currency_names(connection):
    """
    Загрузить названия валют (rus, eng)
    """
    try:
        Logger.info("Добавление данных в currency_name")
        with connection.cursor() as cursor:
            currency_names = [(1,"доллар", "dollar"), (2, "евро", "euro"), (3, "рубль", "rouble"), (4, "юань", "yuan")]
            query = "INSERT INTO currency_name (currency_id, currency_name_rus, currency_name_eng) VALUES(%s, %s, %s)"
            cursor.executemany(query, currency_names)
        connection.commit()
        Logger.info("Добавление данных успешно выполнено")
    except Error:
        Logger.error("Ошибка добавления данных в таблицу",  traceback.format_exc())

Logger = create_logger("DBModel")

#Добавление аргументов командной строки
parser = argparse.ArgumentParser("Взаимодействие с базой данных")
parser.add_argument(
    "-i", "--insert",
    type = str,
    help="Вставка значений в указанную таблицу. По умолчанию - rate",
    default='rate')

#Получение параметров подключения и открытие соединения
user, password, host, port, databases = parse_database_config()
connection = open_connection(user, password, databases["WareHouse"], host, port)

args = parser.parse_args()

if args.insert == "rate":
    if connection:
        _, data = split_col_names_data(read_csv("temp/temp.csv"))
        with connection:
            insert_rates(connection, data)
    else:
        print("Отсутствует соединение с БД")

#Начальное заполнение таблицы. Применять к пустой БД
if args.insert == "example":
    if connection:
        column_names, data = split_col_names_data(read_csv("temp/example.csv"))
        with connection:
            connection.cursor().execute("SET FOREIGN_KEY_CHECKS=0")
            insert_rates(connection, data)
            insert_currencies(connection, column_names[1:])
            insert_currency_names(connection)
            connection.cursor().execute("SET FOREIGN_KEY_CHECKS=1")
    else:
        print("Отсутствует соединение с БД")
