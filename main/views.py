from django.shortcuts import render
import requests
import json
from .models import Config


def index(request):
    rates = {}
    data = json.loads(requests.get('https://back.halykbank.kz/common/currency-history').text)
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
    config = Config.objects.get(id=1)
    telegram = ''
    if config.bot:
        telegram = 'checked'

    gmail = ''
    if config.gmail:
        gmail = 'checked'
    print(telegram)
    return render(request, 'index.html', {'rates': rates, 'telegram': telegram, 'gmail': gmail})
