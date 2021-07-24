#Набор функций для обращения к yaml файлу конфигурации и излвечения из него данных

import yaml
from pathlib import Path

from Logger import create_logger


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
        Logger.info("Чтение файла 'config.yaml' выполнено успешно")       
        return read_data["API_CONNECTION"]
    except FileNotFoundError:
        Logger.error("Файл конфигурации 'config.yaml' не найден.")
        return None

def parse_API_config():
    """
        Получить данные для подключения к API из конфигурационного файла
    """
    config = load_API_config()
    if config:
        url = config["URL"]
        token = config["Token"]
        currency = ",".join(config["Currency"])
        return url, token, currency
    else:
        Logger.error("Не удалось получить данные для подключения к API")

Logger = create_logger("ParseConfig")