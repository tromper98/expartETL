# Осуществляет подключение к API сайта с информацией о курсах валют и 
# выгружает данные в csv файл
import time
import sys
import argparse
import os
import json
import yaml
from datetime import date

import requests 
from requests.models import Response
from requests.exceptions import RequestException

from Logger import create_logger
from ParseConfig import parse_API_config

def send_GET(url, type, params):
    """
        Отправка GET-запроса на URL с указанными параметрами 
    """
    try:
        response = requests.get(url + "/" + type, params)
        if response.ok:
            Logger.info("GET-запрос успешно выполнен")
            return response.json()
    except RequestException:
        Logger.error("Произошла ошибка отправки GET-запроса по адресу ", 
                         url + "/" + type)
        return None

def load_latest_data(url, token, currency):
    """
    Получить самые последние данные об обменном курсе
    """
    Logger.info("Отправка GET-запроса на URL " + url + "/latest")
    request_params = [('access_key', token), ('symbols', currency)]
    #Отправка GET-запроса
    response = send_GET(url, "latest", request_params)
    if response:
        Logger.info("Запрос " + url + "/latest" + "?access_key=" + token + 
                    "symbols=" + currency + " выполнен успешно")
        return response
    else:
        Logger.error("Не удалось выполнить запрос " + url + "/latest" 
                     + "?access_key=" + token + "symbols=" + currency)
        return None

def load_historical_data(url, token, currency, date):
    """
    Получить данные об обменном курсе за указанную дату "yyyy-mm-dd"
    """
    # Проверка корректности переданной даты
    try:
        time.strptime(date, '%Y-%m-%d')
    except ValueError:
        Logger.error('Введена некоректная дата')    
    else:
        #Отправка GET-запроса
        request_params = [('access_key', token), ('symbols', currency)]
        Logger.info("Отправка GET-запроса на URL " + url + "/" + date)
        response = send_GET(url, date, request_params)
        if response:
            Logger.info("Запрос " + url + "/" + date + "?access_key=" + token + 
                    "symbols=" + currency + " выполнен успешно")
            return response
        else:
            Logger.error(" Не удалось выполнить запрос " + url + "/" + date + "?access_key=" + token + 
                    "symbols=" + currency)
            return None

def load_timeseries_data(url, token, currency, start_date, end_date):
    """
    Получить данные об обменном курсе валют за указанный промежуток времени (start_date : end_date) 
    """
    #WARNING Протестировать функцию не представилось возможным, так как сервис не предоставляет
    #данный функционал для пользователей с бесплатным тарифом

    #проверка корректности введенных дат
    try:
        time.strptime(start_date, '%Y-%m-%d')
        time.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        Logger.error('Введены некорректные даты')
    else:
        #отправка GET-запроса
        request_params = [('access_key', token), ("start_date", start_date), 
                          ("end_date", end_date),("symbols", currency)]
        Logger.info("Отправка GET-запроса на URL:" + url + "/timeseries")
        response = send_GET(url, "timeseries", request_params)
        if response:
            Logger.info("Запрос " + url + "/timeseries"  + "?access_key=" + token + "&start_date=" + start_date + 
                        "&end_date=" + end_date + "&symbols=" + currency + " выполнен успешно")
            return response
        else:
            Logger.error("Не удалось выполнить запрос " + url + "/timeseries"  + "?access_key=" + token + "&start_date=" + start_date + 
                        "&end_date=" + end_date + "&symbols=" + currency)
            return None

# проверка, имеются ли в JSON данные или он содержит ошибку 
def check_response(response):
    if response["error"]:
        Logger.error("API вернул ошибк: " + response['error']["message"])
        return False;
    if response["success"]:
        Logger.info("Получены данные в JSON")
        return True;

Logger = create_logger("DataLoader")

#Добавление аргументов командной строки
parser = argparse.ArgumentParser(description="Осуществляет загрузку данных об обменном курсе")
parser.add_argument(
    "-o", "--option", 
    type=str,
    help="Определяет какой тип GET-запроса будет отправлен. По умолчанию: latest",
    default="latest")
parser.add_argument(
    "-d", "--date",
    type=str,
    help="День, накоторый будет загружена информация. Работает в типом hist" 
)
parser.add_argument(
    "-s", "--start_date",
    type=str,
    help="Начальная дата периода",
    default=None)
parser.add_argument(
    "-e", "--end_date",
    type=str,
    help="Конечная дата периода. По умолчанию - текущая дата",
    default=str(date.today()))

args = parser.parse_args()
url, token, currency = parse_API_config()

if args.option == "latest":
    data = load_latest_data(url, token, currency)
if args.option == "hist" and args.date:
    data = load_historical_data(url, token, currency, args.date)
if args.option == "timeseries" and args.start_date:
    data = load_timeseries_data(url, token, currency, args.start_date, args.end_date)



#
#if url:
#    
#    print(data)
#    data = load_historical_data(url, token, currency, "2020-12-30")
#    print(data)





