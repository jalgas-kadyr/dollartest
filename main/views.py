import requests
import json as js
import xlwt
from .models import Config, Check, Change, Interval
from django.shortcuts import render, redirect, HttpResponse

def current_rate():
    rates = {}
    data = js.loads(requests.get('https://back.halykbank.kz/common/currency-history').text)
    res = next(iter(data['data']['currencyHistory']))
    rates = data['data']['currencyHistory'][res]['cards']['USD/KZT']
    return rates

def index(request):
    rates = current_rate()
    config = Config.objects.get(id=1)
    telegram = ''
    if config.bot:
        telegram = 'checked'

    gmail = ''
    if config.gmail:
        gmail = 'checked'

    porogs = {
        'interval': str(config.interval),
        'check': str(config.check),
        'poroginterval': str(config.porog_interval),
        'porogcheck': str(config.porog_check)
    }
    changes = Change.objects.all()

    return render(request, 'index.html', {'rates': rates, 'telegram': telegram, 'gmail': gmail, 'porogs': porogs, 'changes': changes})


def config(request):
    config = Config.objects.get(id=1)
    if len(request.POST['interval']) > 0:
        config.interval = int(request.POST['interval'])
    if len(request.POST['check']) > 0:
        config.check = int(request.POST['check'])
    if len(request.POST['poroginterval']) > 0:
        config.porog_interval = int(float(request.POST['poroginterval']))
    if len(request.POST['porogcheck']) > 0:
        config.porog_check = int(float(request.POST['porogcheck']))

    config.save()
    return redirect('http://127.0.0.1:8000')


def botconfig(request):
    config = Config.objects.get(id=1)
    try:
        print(request.POST['telegram'])
        config.bot = True
        config.save()
    except Exception as error:
        config.bot = False
        config.save()

    try:
        print(request.POST['gmail'])
        config.gmail = True
        config.save()
    except Exception as error:
        config.gmail = False
        config.save()

    api = request.POST['api']
    if len(api) > 0:
        config.API = api
        config.save()

    return redirect('http://127.0.0.1:8000')


def get(request):
    fromdate = str(request.POST['fromdata'])
    fromtime = str(request.POST['fromtime'])
    todate = str(request.POST['todata'])
    totime = str(request.POST['totime'])
    try:
        results = Interval.objects.filter(date__range=[fromdate, todate], time__range=[fromtime, totime])
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('programmist', cell_overwrite_ok=True)
        ws.write(0, 0, '№')
        ws.write(0, 1, 'DateTime')
        ws.write(0, 2, 'Time')
        ws.write(0, 3, 'Sell')
        ws.write(0, 4, 'Buy')
        print(results)
        i = 1
        for result in results:
            ws.write(i, 0, result.id)
            ws.write(i, 1, str(result.date))
            ws.write(i, 2, str(result.time))
            ws.write(i, 3, result.sell)
            ws.write(i, 4, result.buy)
            i = i + 1

        wb.save('dollar.xls')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Report.xls'
        wb.save(response)
        return response
    except Exception as error:
        pass
    return redirect('http://127.0.0.1:8000')


