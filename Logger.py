#Класс для логирования действий, совершаемых скриптами
from pathlib import Path

class Logger:
    """
    Реализует логирование событий 
    """
    __filePath = ""
    logger = None
    
    #Создание логгера
    def __init__(self, logger_name):
        import logging
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        myself = Path(__file__).resolve()
        self.__filepath = myself.parents[1] / log.log

        try:
            fh = logging.FileHandler(self.__filePath)
        except FileNotFoundError:
            log_path = 'log.log'
            fh = logging.FileHandler(log_path)

        # Формат записи логов    
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
    #@staticmethod
    def add(self, message):
        self.logger.info(str(message))
    
    #@staticmethod
    def add_error(self, message):
        self.logger.error(str(message))
    
    #@staticmethod
    def add_warning(self, message):
        self.logger.warning(str(message))
    
    #@staticmethod
    def add_critical(self, message):
        self.logger.critical(str(message))

    #@staticmethod
    def add_debug(self, message):
        self.logger.debug(str(message))
        
if __name__ == "__main__":
    pass