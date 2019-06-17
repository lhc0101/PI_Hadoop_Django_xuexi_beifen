from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests as rts
from my_iot.models import HistoryValue
from django.conf import settings

def getValue():
    t = ''
    h = ''
    s = ''
    g = ''
    if settings.CURRENT_TEMPERATURE == None:
        t = "无读数"
    else:
        t = str(settings.CURRENT_TEMPERATURE)
    if settings.CURRENT_HUMIDITY == None:
        h = "无读数"
    else:
        h = str(settings.CURRENT_HUMIDITY)
    if settings.CURRENT_SHIDU == None:
        s = "无读数"
    else:
        s = str(settings.CURRENT_SHIDU)
    if settings.CURRENT_GUANGZHAO == None:
        g = "无读数"
    else:
        g = str(settings.CURRENT_GUANGZHAO)
    return t, h, s, g

def index(request):
    t, h, s, g = getValue()
    return render(request, 'my_iot/index.html', {'t':t, 'h':h, 's':s, 'g':g})

@csrf_exempt
def communicate(request):
    if 'method' in request.GET:
        method = request.GET['method']
        data = request.GET['data']
        rts.get("http://127.0.0.1:3000/com" + "?data=" + data)
        return HttpResponse("ok")
    elif 'method' in request.POST:
        method = request.POST['method']
        data = request.POST['data']
        rts.post("http://127.0.0.1:3000/com", data={'data':data})
        return HttpResponse("ok")
    elif 'data' in request.GET:
        data = request.GET['data']
        print("I'm django received get data: " + data)
        return HttpResponse("ok")
    elif 'data' in request.POST:
        data = request.POST['data']
        print("I'm django received post data: " + data)
        return HttpResponse("ok")
    return render(request, 'my_iot/communicate.html')

@csrf_exempt
def data(request):
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}, {1}, {2}, {3}".format(d['t'], d['h'], d['s'], d['g']))
        value = HistoryValue(temperature=d['t'], humidity=d['h'],shidu=d['s'],guangzhao=d['g'])
        value.save()
        settings.CURRENT_TEMPERATURE = d['t']
        settings.CURRENT_HUMIDITY = d['h']
        settings.CURRENT_SHIDU = d['s']
        settings.CURRENT_GUANGZHAO = d['g']
    if 'get' in request.GET:
        rts.get("http://192.168.137.6:5000" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        t, h, s, g = getValue()
        return HttpResponse(json.dumps({'t': t, 'h': h, 's': s, 'g':g}))
    return HttpResponse("ok")

def detail_page(request):
    return render(request,'my_iot/detail.html')

def login_page(request):
    return render(request,'my_iot/login.html')
def register_page(request):
    return render(request,'my_iot/register.html')