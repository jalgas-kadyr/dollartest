from datetime import datetime

import requests
import json

data = json.loads(requests.get('https://back.halykbank.kz/common/currency-history').text)
dt = str(datetime.now())
print(dt[11] + dt[12])