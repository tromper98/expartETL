#Набор функций для обращения к yaml файлу конфигурации и излвечения из него данных

import yaml
from pathlib import Path

from Logger import Logger

def load_API_config():
    """
    Загрузка параметров подключения к API сайта (URL, token) 
    и списка валют 
    """
    try:
        myself = Path(__file__).resolve()
        path = myself.parents[1] / 'config.yaml'
        with open(path) as cf:
            read_data = yaml.safe_load(cf)
        return read_data["API_CONNECTION"]
    except FileNotFoundError:
        Logger.add_error("Файл конфигурации 'config.yaml' не найден.")
        return None

def parse_API_config():
    """
        Получить данные для подключения к API из конфигурационного файла
    """
    config = load_API_config()
    url = config["URL"]
    token = config["Token"]
    print(token)
    currency = ",".join(config["Currency"])
    return url, token, currency

print(parse_API_config())

Logger = Logger("log")