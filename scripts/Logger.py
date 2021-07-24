import logging
from pathlib import Path
 
def create_logger(logger_name):
    """
    Реализует логирование событий 
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    myself = Path(__file__).resolve()
    filePath = myself.parents[1] / "app.log"
    fh = logging.FileHandler(filePath)
    # Формат записи логов    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
    
if __name__ == "__main__":
    pass