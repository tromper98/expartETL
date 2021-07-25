#Обработчик CSV-файлов. Осуществляет чтение и запись данных. 

import logging
import os
import csv

from Logger import create_logger

#Запись данных в csv-файл
def write_to_csv(filename, data):
    Logger.info("Запись в файл " + filename)

    #Создаем временным файл, если он не найден в дирректории
    if not os.path.exists(filename):
        with open(filename, mode="w", encoding='UTF-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            ls = ["date"]
            ls.extend(get_currency_keys(data)) 
            file_writer.writerow(ls)

    #Запись данных в temp.csv
    with open(filename, mode="a", encoding='UTF-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        for key in data:
            ls = [key]
            ls.extend(list(data[key].values()))
            file_writer.writerow(ls)
    Logger.info("Запись в " + filename + " завершена")    

#Чтение csv-файла
def read_csv(filename):
    try:
        Logger.info("Чтение файла " + filename)
        rows = []
        with open(filename, "r", encoding="UTF-8") as r_file:
            file_reader = csv.reader(r_file, delimiter=";", lineterminator="\r")
            for row in file_reader:
                rows.append(row)
        Logger.info("Чтение файла " + filename + " завершено")
        return rows
    except FileNotFoundError:
        Logger.error("Ошибка чтения файла. Файл " + filename + " не найден")
        return None

#Получить список валют из словаря
def get_currency_keys(dict):
    keys = list(dict.keys())
    nested_keys = list()
    for nested_key in dict[keys[0]]:
        nested_keys.append(nested_key)
    return nested_keys

#разделить список на два: наименования столбцов и данные
def split_col_names_data(list):
    return list[0], list[1:] 
    
Logger = create_logger("CSVHandler")

