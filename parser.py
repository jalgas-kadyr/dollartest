from datetime import datetime

import requests
import json

data = json.loads(requests.get('https://back.halykbank.kz/common/currency-history').text)

rates = {}
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

print(data)