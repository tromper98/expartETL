# Осуществляет подключение к API сайта с информацией о курсах валют и 
# выгружает данные в csv файл
import time
import argparse
import json
import traceback
from datetime import date, timedelta

import requests 
from requests.exceptions import RequestException

from Logger import create_logger
from ParseConfig import parse_API_config
from CSVHandler import write_to_csv

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
                         url + "/" + type, traceback.format_exc())
        return None

# проверка, имеются ли в JSON данные или он содержит ошибку 
def check_response(response):
    if "error" in response:
        Logger.error("API вернул ошибк: " + response['error']["message"])
        return False;
    else:
        Logger.info("Получены данные в JSON")
        return True;

def load_latest_data(url, token, base, currency):
    """
    Получить самые последние данные об обменном курсе
    """
    Logger.info("Отправка GET-запроса на URL " + url + "/latest")
    request_params = [('access_key', token), ('base', base), ('symbols', currency)]
    #Отправка GET-запроса
    response = send_GET(url, "latest", request_params)
    if response:
        Logger.info("Запрос " + url + "/latest" + "?access_key=" + token + 
                    "&base=" + base + "&symbols=" + currency + " выполнен успешно")
        return response
    else:
        Logger.error("Не удалось выполнить запрос " + url + "/latest" 
                     + "?access_key=" + token + "&base=" + base + "&symbols=" + currency,  traceback.format_exc())
        return None

def load_historical_data(url, token, base, currency, date):
    """
    Получить данные об обменном курсе за указанную дату "yyyy-mm-dd"
    """
    # Проверка корректности переданной даты
    try:
        time.strptime(date, '%Y-%m-%d')
    except ValueError:
        Logger.error('Введена некоректная дата',  traceback.format_exc())    
    else:
        #Отправка GET-запроса
        request_params = [('access_key', token), ('base', base), ('symbols', currency)]
        Logger.info("Отправка GET-запроса на URL " + url + "/" + date)
        response = send_GET(url, date, request_params)
        if response:
            Logger.info("Запрос " + url + "/" + date + "?access_key=" + token + 
                    "symbols=" + currency + " выполнен успешно")
            return response
        else:
            Logger.error(" Не удалось выполнить запрос " + url + "/" + date + "?access_key=" + token + 
                    "$symbols=" + currency,  traceback.format_exc())
            return None

def load_timeseries_data(url, token, base, currency, start_date, end_date):
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
        Logger.error('Введены некорректные даты',  traceback.format_exc())
    else:
        #отправка GET-запроса
        request_params = [('access_key', token), ('base', base), ("start_date", start_date), 
                          ("end_date", end_date),("symbols", currency)]
        Logger.info("Отправка GET-запроса на URL:" + url + "/timeseries")
        response = send_GET(url, "timeseries", request_params)
        if response:
            Logger.info("Запрос " + url + "/timeseries"  + "?access_key=" + token + "&start_date=" + start_date + 
                        "&end_date=" + end_date + "&symbols=" + currency + " выполнен успешно")
            return response
        else:
            Logger.error("Не удалось выполнить запрос " + url + "/timeseries"  + "?access_key=" + token + "&start_date=" + start_date + 
                        "&end_date=" + end_date + "&symbols=" + currency,  traceback.format_exc())
            return None

#Загружает данные за последние полгода для наполнения DWH
#Использует единичные GET-запросы на конкретную дату
#Сделано для того, чтобы обойти ограничения бесплатной версии API   
def load_example_data(url, token, base, currency):
    """
    Загрузка данных для начального наполнения БД 
    """
    #Итератор по датам.
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    start_date = date.today() - timedelta(180)
    #Итеративное обращение к API
    for single_date in daterange(start_date, date.today()):
        json = load_historical_data(url, token, base, currency, single_date.strftime("%Y-%m-%d"))
        data = convert_JSON(json)
        write_to_csv("temp/example.csv", data)
        
Logger = create_logger("DataLoader")
convert_JSON = lambda json: {json["date"] : json["rates"]} #Конвертировать JSON в формат: {date :{"cur_name1" : num1, "cur_name2" : num2 ...}} 
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
url, token, base, currency = parse_API_config()

#Проверка переданного аргумента и вызов соответствующего GET-запроса
if args.option == "latest":
    json = load_latest_data(url, token, base, currency)
    data = convert_JSON(json)
if args.option == "hist" and args.date:
    json = load_historical_data(url, token, base, currency, args.date)
    data = convert_JSON(json)
if args.option == "timeseries" and args.start_date:
    json = load_timeseries_data(url, token, base, currency, args.start_date, args.end_date)
    data = json["rates"]
if args.option == "example":
    load_example_data(url, token, base, currency)

#Если данные были получены, то сохраняем в csv-файл
if args.option != "example" and check_response(data):
    write_to_csv("temp/temp.csv", data)
