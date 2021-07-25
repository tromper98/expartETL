#Обработчик CSV-файлов. Осуществляет чтение и запись данных. 

import logging
import os
import csv

from Logger import create_logger

#Запись данных в csv-файл
def write_to_csv(filename, data):
    Logger.info("Запись в файл ", filename)

    if not os.path.exists("temp.csv"):
        with open(filename, mode="w", encoding='UTF-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            ls = ["date"] + list(data['rates'].keys())
            file_writer.writerow(ls)

    try:
        with open(filename, mode="a", encoding='UTF-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            ls = list()
            ls.append(data["date"])
            ls.extend(data["rates"].values())
            file_writer.writerow(ls)
        Logger.info("Запись в", filename, "завершена")
    except FileExistsError:
        Logger.error("Ошибка записи данных в файл")        

#Чтение csv-файла
def read_csv(filename):
    pass

Logger = create_logger("CSVHandler")
data = { 'date' : "2020-10-15",
         'rates':{
                "USD":1.17713,
                "AUD":1.598276,
                "CAD":1.479005,
                "PLN":4.574387,
                "MXN":23.610227
  }}

write_to_csv('temp.csv', data)
print(data["date"])
ls = ["date"]
print(ls)
print(ls + list(data['rates'].keys()))
print()
