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


# print(data['data']['currencyHistory'])

data = {
    'test': 1,
    'test2': 2
}
res = next(iter(data))
print(res)