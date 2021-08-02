#Обработчик CSV-файлов. Осуществляет чтение и запись данных. 

import traceback
import os
import csv
import argparse
from typing import Union, List, Dict, Any
from Logger import create_logger


#Запись данных в csv-файл
def write_to_csv(filename: str, data: Dict[str, str]) -> None:
    Logger.info("Запись в файл " + filename)
    #Создаем временным файл, если он не найден в дирректории
    if not os.path.exists(filename):
        with open(filename, mode="w", encoding='UTF-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            ls: List[str] = ["date"]
            ls.extend(get_currency_keys(data)) 
            file_writer.writerow(ls)

    #Запись данных в temp.csv
    with open(filename, mode="a", encoding='UTF-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        for key in data:
            ls: List[float] = [key]
            ls.extend(list(data[key].values()))
            file_writer.writerow(ls)
    Logger.info("Запись в " + filename + " завершена")    

#Чтение csv-файла
def read_csv(filename: str) ->Union[List[Any], None]:
    try:
        Logger.info("Чтение файла " + filename)
        rows: List[str, float] = []
        with open(filename, "r", encoding="UTF-8") as r_file:
            file_reader = csv.reader(r_file, delimiter=";", lineterminator="\r")
            for row in file_reader:
                rows.append(row)
        Logger.info("Чтение файла " + filename + " завершено")
        return rows
    except FileNotFoundError:
        Logger.error("Ошибка чтения файла. Файл " + filename + " не найден",  traceback.format_exc())
        return None

#Получить список валют из словаря
def get_currency_keys(dict: Dict[str, str]) -> List:
    keys: List[str] = list(dict.keys())
    nested_keys: List[str] = list()
    for nested_key in dict[keys[0]]:
        nested_keys.append(nested_key)
    return nested_keys

#разделить список на два: наименования столбцов и данные
def split_col_names_data(list: List[Any]):
    return list[0], list[1:] 

#Удаление файла с именем filename   
def remove_file(filename: str):
    if os.path.exists(filename):
        Logger.info("Удаление файла" +filename)
        os.remove(filename)
Logger = create_logger("CSVHandler")

parser: argparse.ArgumentParser = argparse.ArgumentParser()

parser.add_argument(
    "-r", "--remove",
    type=str,
    help="Удалить файл temp",
    default="temp"
)

args: argparse.Namespace = parser.parse_args()

if args.remove == "temp":
    remove_file("temp/temp.csv")