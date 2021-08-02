#Набор функций для обращения к yaml файлу конфигурации и извлечения из него данных
import traceback
from typing import Dict, List, Any, Union
import yaml
from pathlib import Path
from dataclasses import dataclass

from Logger import create_logger

#DTO для хранения параметров подлючения к API веб-сервера с курсами валют
@dataclass
class API_config:
    url: str
    token: str
    base: str
    currency: List[str]

#DTO для хранения параметров подключения к СУБД MySQL
@dataclass
class DB_config:
    user: str
    password: str 
    host: str
    port: str
    databases: str

def read_config(section : str) -> Union[Dict, None]:
    """
    Чтение конфигурационного файла. возвращает указанную секцию файла  
    """
    try:
        myself: Path = Path(__file__).resolve()
        path: str = myself.parents[1] / 'config.yaml'
        with open(path) as cf:
            read_data: Dict = yaml.safe_load(cf)
        Logger.info("Чтение файла 'config.yaml' выполнено успешно")       
        return read_data[section]
    except FileNotFoundError:
        Logger.error("Файл конфигурации 'config.yaml' не найден.",  traceback.format_exc())
        return None

#Читает config.yaml и возвращает секцию API_CONNECTION 
def load_API_config() -> Union[Dict, None]:
    """
    Загрузка параметров подключения к API сайта (URL, token) 
    и списка валют 
    """
    api_config: Union[Dict, None]= read_config("API_CONNECTION")
    if (api_config):
        return api_config
    else:
        return None


#Парсит полученную секцию из load_API_config и возвращает параметры поэлементно
def parse_API_config()-> Union[API_config, None]:
    """
    Получить данные для подключения к API из конфигурационного файла
    """
    config: Union[Dict, None] = load_API_config()
    if config:
        API_params: API_config = API_config(config["URL"], config["Token"], config["Base"], ",".join(config["Currency"]))
        return API_params
    else:
        Logger.error("Не удалось получить данные для подключения к API",  traceback.format_exc())

#Получает данные для подключения к БД из config.yaml
def load_database_config() -> Union[Dict, None]:
    """
    Получить параметры подключения к БД из файла конфигурации
    """
    database_config: Union[Dict, None] = read_config("DATABASE")
    if database_config:
        return database_config
    else:
        return None

#парсер конфигурации подключения к базе данных
def parse_database_config() -> Union[DB_config, None]:
    """
    Извлечение данных о подключения к базе данных
    """
    config: Union[Dict, None] = load_database_config()
    if config:
        DB_params: DB_config = DB_config(config["Host"], config["UserName"], config["Password"],
                              config["Port"], config["Databases"])
        return  DB_params
    else:
        Logger.error("Не удалось получить данные о подключении к БД",  traceback.format_exc())
        return None

Logger = create_logger("ParseConfig")
