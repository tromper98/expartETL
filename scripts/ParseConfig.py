#Набор функций для обращения к yaml файлу конфигурации и извлечения из него данных
import traceback
import yaml
from pathlib import Path

from Logger import create_logger

def read_config(section):
    """
    Чтение конфигурационного файла. возвращает указанную секцию файла  
    """
    try:
        myself = Path(__file__).resolve()
        path = myself.parents[1] / 'config.yaml'
        with open(path) as cf:
            read_data = yaml.safe_load(cf)
        Logger.info("Чтение файла 'config.yaml' выполнено успешно")       
        return read_data[section]
    except FileNotFoundError:
        Logger.error("Файл конфигурации 'config.yaml' не найден.",  traceback.format_exc())
        return None

#Читает config.yaml и возвращает секцию API_CONNECTION 
def load_API_config():
    """
    Загрузка параметров подключения к API сайта (URL, token) 
    и списка валют 
    """
    api_config = read_config("API_CONNECTION")
    if (api_config):
        return api_config
    else:
        return None


#Парсит полученную секцию из load_API_config и возвращает параметры поэлементно
def parse_API_config():
    """
    Получить данные для подключения к API из конфигурационного файла
    """
    config = load_API_config()
    if config:
        url = config["URL"]
        token = config["Token"]
        currency = ",".join(config["Currency"])
        base = config["Base"]
        return url, token, base, currency
    else:
        Logger.error("Не удалось получить данные для подключения к API",  traceback.format_exc())

#Получает данные для подключения к БД из config.yaml
def load_database_config():
    """
    Получить параметры подключения к БД из файла конфигурации
    """
    database_config = read_config("DATABASE")
    if database_config:
        return database_config
    else:
        return None

#парсер конфигурации подключения к базе данных
def parse_database_config():
    """
    Извлечение данных о подключения к базе данных
    """
    config = load_database_config()
    if config:
        host = config["Host"]
        user = config["UserName"]
        password = config["Password"]
        port = config["Port"]
        databases = config["Databases"]
        return  user, password, host, port, databases
    else:
        Logger.error("Не удалось получить данные о подключении к БД",  traceback.format_exc())

Logger = create_logger("ParseConfig")

