# Осуществляет подключение к API сайта с информацией о курсах валют и 
# выгружает данные в csv файл

import yaml

import pandas as pd
import requests as rq
from yaml.loader import Loader


def load_API_config():
    """
    Загрузка параметров подключения к API сайта (URL, token) 
    и списка валют 
    """
    with open("config.yaml") as cf:
        read_data = yaml.safe_load(cf)
    return read_data["API_CONNECTION"]


