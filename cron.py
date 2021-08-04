#Планировщик заданий cron
from scripts.CSVHandler import remove_file
from crontab import CronTab
cron = CronTab(tab="* * * * * command")

#Запуск скрипта для загрузки данных с API сервера
load_currency = cron.new(command="python ./scripts/DataLoader.py -o latest")
load_currency.setall('0 8 * * *')

#Запуск скрипта для вставки данных в базу данных
insert_data = cron.new(command="python ./scripts/DBModel.py -i rate")
insert_data.setall('1 8 * * *')

#Запуск скрипта на удаление temp файла
remove_file = cron.new(command="python ./scripts/CSVHandler.py -r temp")
remove_file('2 8 * * *')

cron.write()