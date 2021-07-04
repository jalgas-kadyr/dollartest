import requests
import json
import datetime
import django
import telebot
from time import sleep, time
from django.conf import settings
from dollaranalityc.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()
from main.models import *


def current_rate(banks):
    rates = {}
    for bank in banks:
        if bank == 'halyk':
            data = json.loads(requests.get('https://back.halykbank.kz/common/currency-history').text)
            try:
                rates[bank] = data['data']['currencyHistory']['1']['cards']['USD/KZT']
            except Exception as error:
                print('Error: ', error)
                rates[bank] = data['data']['currencyHistory'][1]['cards']['USD/KZT']
            except Exception as error:
                print(error)
                rates[bank] = data['data']['currencyHistory']['0']['cards']['USD/KZT']
            except Exception as error:
                print(error)
                rates[bank] = data['data']['currencyHistory']['1']['cards']['USD/KZT']
            except Exception as error:
                print(error)
    return {'halyk': data['data']['currencyHistory']['1']['cards']['USD/KZT']}

def get_result():
    result = Result()
    result.buy = current_rate('halyk')['buy']
    result.sell = current_rate('halyk')['sell']
    result.date = datetime.datetime.now()


def get_banks(config):
    banks = []
    bank = ''
    for i in config.banks:
        if i == ',':
            banks.append(bank)
            bank = ''
        else:
            bank = bank + i
    return banks


def check():
    result = Result.objects.order_by('-id')[0]
    last = Result.objects.order_by('-id')[1]
    message = ''
    if result.sell != last.sell or result.buy != last.buy:
        dfbp = 100 - ((result.buy * 100) / last.buy)
        dfsp = 100 - ((result.sell * 100) / last.sell)
        dfbtg = result.buy - last.buy
        dfstg = result.sell - last.sell
        change = True

    if change:
        if result.sell != last.sell:
            message = message + 'Курс продажи доллара изменился на ' + str(dfsp) + '%/' + str(dfstg) + 'KZT\n'
        if result.buy != last.buy:
            message = message + 'Курс покупки доллара изменился на ' + str(dfbp) + '%/' + str(dfbtg) + 'KZT\n'

        message = message + 'Текущий курс: \nПродажа - ' + result.sell + '\n' + 'Покупка' + str(result.buy)
        bot.send_message(config.jalgas, message)
    print(last.unix)
    print(result .unix)


config = Config.objects.get(id=1)
iteration = config.iteration
bot = telebot.TeleBot(config.API)

while True:
    config = Config.objects.get(id=1)
    dt = str(datetime.datetime.now())
    hour = int(dt[11] + dt[12])
    min = int(dt[14] + dt[15])
    if min % config.interval == 0:
        banks = get_banks(config)
        result = Result(
            buy=current_rate(banks)['halyk']['buy'],
            sell=current_rate(banks)['halyk']['sell'],
            date=datetime.date.today(),
            time=datetime.datetime.now().strftime('%H:%M:%S'),
            unix=int(time())
        )
        result.save()
        sleep(60)
    if ((hour * 60) + min) % config.check == 0:
        check()
        sleep(60)


