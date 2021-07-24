# Осуществляет подключение к API сайта с информацией о курсах валют и 
# выгружает данные в csv файл


import time
import sys
import argparse

import yaml
import pandas as pd
import requests 
from requests.models import Response
from requests.exceptions import RequestException

from Logger import Logger
from ParseConfig import parse_API_config

def send_GET(url, type, params):
    """
        Отправка GET-запроса на URL с указанными параметрами 
    """
    try:
        response = requests.get(url + "/" + type, params)
        if response.ok:
            Logger.add("GET-запрос успешно выполнен")
            return response.json()
    except RequestException:
        Logger.add_error("Произошла ошибка отправки GET-запроса по адресу ", 
                         url + "/" + type)
        return None

def load_latest_data(url, token, currency):
    """
    Получить самые последние данные об обменном курсе
    """
    Logger.add("Отправка GET-запроса на URL " + url + "/latest")
    request_params = [('access_key', token), ('symbols', currency)]
    #Отправка GET-запроса
    response = send_GET(url, "latest", request_params)
    if response:
        Logger.add("Запрос " + url + "/latest" + "?access_key=" + token + 
                    "symbols=" + currency + " выполнен успешно")
        return response
    else:
        Logger.add_error("Не удалось выполнить запрос " + url + "/latest" 
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
        Logger.add_error('Введена некоректная дата')    
    else:
        #Отправка GET-запроса
        request_params = [('access_key', token), ('symbols', currency)]
        Logger.add("Отправка GET-запроса на URL " + url + "/" + date)
        response = send_GET(url, date, request_params)
        if response:
            Logger.add("Запрос " + url + "/" + date + "?access_key=" + token + 
                    "symbols=" + currency + " выполнен успешно")
            return response
        else:
            Logger.add_error(" Не удалось выполнить запрос " + url + "/" + date + "?access_key=" + token + 
                    "symbols=" + currency)
            return None

Logger = Logger("log")

url, token, currency = parse_API_config()
if url:
    data = load_latest_data(url, token, currency)
    print(data)
    data = load_historical_data(url, token, currency, "2020-12-30")
    print(data)





