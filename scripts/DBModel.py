#Функции взаимодействия с БД MySql
#выполняют подключение и загрузку данных в БД
import argparse
import os
from datetime import  datetime
import traceback
from typing import Optional, List, Any
from mysql.connector.connection import MySQLConnection


import numpy as np
from mysql.connector import connect, Error
from logging import Logger

from ParseConfig import parse_database_config, DB_config
from Logger import create_logger
from CSVHandler import read_csv, split_col_names_data


#Подлючение к базе данных
def open_connection(DB_config: DB_config) -> Optional[MySQLConnection]:
    """
    Подключение к базе данных в MySQL
    """
    try:
        Logger.info("Подключение к базе данных " + DB_config.databases["WareHouse"])
        connection: Optional[MySQLConnection] = connect(user=DB_config.user, password=DB_config.password, 
                        database=DB_config.databases["WareHouse"], host=DB_config.host, port=DB_config.port, buffered = True)
        return connection
    except Error:
        Logger.error("Ошибка подключения к базе данных " + DB_config.databases["WareHouse"],  traceback.format_exc())
        return None

#Вставка валютных знаков в таблицу currency
#Поле currency_load_datetime заполняется с помощью вызова триггера before insert
def insert_currencies(connection: MySQLConnection, currency_codes: List[str]) -> None:
    """
    Вставка валютных знаков в БД    
    """
    try:
        Logger.info("Запись данных в таблицу currency")
        with connection.cursor() as cursor:
            query: str = "INSERT INTO currency (currency_id, currency_code) VALUES (%s, %s);"
            for currency_code in currency_codes:
                cursor.execute(query, (None, currency_code))      
                connection.commit()
        Logger.info("Запись данных успешно завершена")
    except Error:
       Logger.error("Ошибка записи данных в таблицу currency. Ошибка: ",  traceback.format_exc())

#Вставка значений курса валют из временного файла temp.csv
#Поле rate_load_datetime заполняется через триггер before insert 
def insert_rates(connection: MySQLConnection, data: List[Any]) -> None:
    """
    Вставка информации об изменении курса валют
    """
    #разбиваем матрицу на массив дат и массив курсов
    data: np.array = np.array(data)
    dates: List[str] = data[:, 0]
    rates: List[float] = data[:, 1:]
    try: 
        Logger.info("Начало записи данных в таблицу rate")
        with connection.cursor() as cursor:
            query: str = "INSERT INTO rate (rate_currency_id, rate_date, rate_value) VALUES (%s, %s, %s);"
            for i in range(len(dates)):
                key: int = 1
                for rate in rates[i, :]:
                    tp: tuple(int, datetime, float) = (key,  datetime.strptime(dates[i], "%Y-%m-%d").date(), float(rate))
                    key += 1
                    cursor.execute(query, tp)
            connection.commit()
        Logger.info("Запись данных успешно завершена")
    except Error:
        Logger.error("Ошибка записи данных в таблицу rate",  traceback.format_exc())

#Вставка названий валют на русском и английском языках
def insert_currency_names(connection: MySQLConnection) -> None:
    """
    Загрузить названия валют (rus, eng)
    """
    try:
        Logger.info("Добавление данных в currency_name")
        with connection.cursor() as cursor:
            currency_names: List[tuple[int, str, str, str]] = [
                              (1,"доллар", "dollar", "dollar", "美元" ), 
                              (2, "евро", "euro", "euro", "欧元"), 
                              (3, "рубль", "rouble", "rubel", "卢布"), 
                              (4, "юань", "yuan", "yuan", "人民币")
                              ]
            query: str = """INSERT INTO currency_name 
                       (currency_id, currency_name_rus, currency_name_eng, 
                       currency_name_deu, currency_name_chi)
                       VALUES(%s, %s, %s, %s, %s)"""
            cursor.executemany(query, currency_names)
        connection.commit()
        Logger.info("Добавление данных успешно выполнено")
    except Error:
        Logger.error("Ошибка добавления данных в таблицу",  traceback.format_exc())

Logger = create_logger("DBModel")

#Добавление аргументов командной строки
parser: argparse.ArgumentParser = argparse.ArgumentParser("Взаимодействие с базой данных")
parser.add_argument(
    "-i", "--insert",
    type = str,
    help="Вставка значений в указанную таблицу. По умолчанию - rate",
    default=None)

#Получение параметров подключения и открытие соединения
DB_config: DB_config = parse_database_config()
connection: MySQLConnection = open_connection(DB_config)

args: argparse.Namespace = parser.parse_args()

if args.insert == "rate":
    if connection:
        _, data = split_col_names_data(read_csv(os.path.join("/", "tmp", "expart.csv")))
        with connection:
            insert_rates(connection, data)
    else:
        print("Отсутствует соединение с БД")
        Logger.error("Отсутствует соединение с БД",  traceback.format_exc())

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
        Logger.error("Отсутствует соединение с БД",  traceback.format_exc())
