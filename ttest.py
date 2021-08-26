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

config = Config.objects.last()
bot = telebot.TeleBot(config.API)


def current_rate():
    rates = {}
    data = json.loads(requests.get('https://back.halykbank.kz/common/currency-history').text)
    res = next(iter(data['data']['currencyHistory']))
    try:
        rates = data['data']['currencyHistory']['3']['cards']['USD/KZT']
    except Exception as error:
        try:
            rates = data['data']['currencyHistory'][1]['cards']['USD/KZT']
        except Exception as error:
            try:
                rates = data['data']['currencyHistory']['0']['cards']['USD/KZT']
            except Exception as error:
                try:
                    rates = data['data']['currencyHistory'][0]['cards']['USD/KZT']
                except Exception as error:
                    try:
                        rates = data['data']['currencyHistory']['2']['cards']['USD/KZT']
                    except Exception as error:
                        try:
                            rates = data['data']['currencyHistory'][2]['cards']['USD/KZT']
                        except Exception as error:
                            pass


def interval():
    interval = Interval(
        buy=current_rate()['buy'],
        sell=current_rate()['sell'],
        # buy=float(input('buy: ')),
        # sell=float(input('sell: ')),
        date=datetime.date.today(),
        time=datetime.datetime.now().strftime('%H:%M:%S'),
        unix=int(time())
    )
    check_interval(interval)
    print(current_rate())


def check_interval(interval):
    last = Interval.objects.last()
    interval.save()
    message = ''
    config = Config.objects.last()
    if interval.buy != last.buy or interval.sell != last.sell:
        dfbp = 100 - ((interval.buy * 100) / last.buy)
        dfsp = 100 - ((interval.sell * 100) / last.sell)
        dfbtg = interval.buy - last.buy
        dfstg = interval.sell - last.sell
        if dfstg > config.porog_interval  or dfstg < config.porog_interval:
            message = message + 'Курс продажи доллара изменился на ' + str(round(dfstg, 2)) + 'KZT за послдение ' + str(
                config.interval) + ' минут\n'
        if  dfbtg > config.porog_interval  or dfstg < dfbtg.porog_interval:
            message = message + 'Курс купли доллара изменился на ' + str(round(dfbtg, 2)) + 'KZT за послдение ' + str(
                config.interval) + ' минут\n'

        message = message + 'Текущий курс: \nПродажа - ' + str(current_rate()['sell']) + '\nПокупка - ' + str(
            current_rate()['buy'])
        change = Change(
            buy=interval.buy,
            sell=interval.sell,
            dfsp=dfsp,
            dfbp=dfbp,
            dfstg=dfstg,
            dfbtg=dfbtg,
            date=interval.date,
            time=interval.time,
            unix=interval.unix,
            big=False
        )
        change.save()
        if send:
            bot.send_message(config.jalgas, message)
            bot.send_message(config.galymjan, message)


def big_check():
    last = Check.objects.last()
    check = Check(
        buy=current_rate()['buy'],
        sell=current_rate()['sell'],
        # buy=float(input('big_buy: ')),
        # sell=float(input('big_sell: ')),
        date=datetime.date.today(),
        time=datetime.datetime.now().strftime('%H:%M:%S'),
        unix=int(time())
    )
    check.save()
    config = Config.objects.last()
    message = ''
    if check.buy != last.buy or check.sell != last.sell:
        dfbp = 100 - ((check.buy * 100) / last.buy)
        dfsp = 100 - ((check.sell * 100) / last.sell)
        dfbtg = check.buy - last.buy
        dfstg = check.sell - last.sell
        if dfstg != 0.0:
            message = message + 'Курс продажи доллара изменился на ' + str(round(dfstg, )) + 'KZT за послдение ' + str(
                config.check) + ' минут\n'
        if dfbtg != 0.0:
            message = message + 'Курс купли доллара изменился на ' + str(round(dfbtg, 2)) + 'KZT за послдение ' + str(
                config.check) + ' минут\n'

        message = message + 'Текущий курс: \nПродажа - ' + str(current_rate()['sell']) + '\nПокупка - ' + str(
            current_rate()['buy'])
        change = Change(
            buy=check.buy,
            sell=check.sell,
            dfsp=dfsp,
            dfbp=dfbp,
            dfstg=dfstg,
            dfbtg=dfbtg,
            date=check.date,
            time=check.time,
            unix=check.unix,
            big=True
        )
        change.save()
        if send:
            bot.send_message(config.jalgas, message)
            bot.send_message(config.galymjan, message)


while True:
    config = Config.objects.get(id=1)
    send = config.bot
    dt = str(datetime.datetime.now())
    hour = int(dt[11] + dt[12])
    min = int(dt[14] + dt[15])

    if min % config.interval == 0:
        interval()

    if ((hour * 60) + min) % config.check == 0:
        big_check()

    sleep(60)
