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
    Temp = ''
    Pressure = ''
    Altitude = ''
    Sealevel_Pressure = ''
    rade_data = ''
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
    if settings.CURRENT_TEMP == None:
        Temp = "无读数"
    else:
        Temp = str(settings.CURRENT_TEMP)
    if settings.CURRENT_PRESSURE == None:
        Pressure = "无读数"
    else:
        Pressure = str(settings.CURRENT_PRESSURE)
    if settings.CURRENT_ALTITUDE == None:
        Altitude = "无读数"
    else:
        Altitude = str(settings.CURRENT_ALTITUDE)
    if settings.CURRENT_SEALEVEL_PRESSURE == None:
        Sealevel_Pressure = "无读数"
    else:
        Sealevel_Pressure = str(settings.CURRENT_SEALEVEL_PRESSURE)
    if settings.CURRENT_DATA == None:
        rade_data = "无读数"
    else:
        rade_data = str(settings.CURRENT_DATA)
    return t, h, s, g , Temp , Pressure , Altitude ,Sealevel_Pressure ,rade_data

def index(request):
    t, h, s, g ,Temp , Pressure , Altitude ,Sealevel_Pressure , rade_data = getValue()
    return render(request, 'my_iot/index.html', {'t':t, 'h':h, 's':s, 'g':g,"Temp":Temp,"Pressure":Pressure,"Altitude":Altitude,"Sealevel_Pressure":Sealevel_Pressure , "rade_data":rade_data})

@csrf_exempt
def data(request):
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}, {1}, {2}, {3},{4},{5},{6},{7}".format(d['t'], d['h'], d['s'], d['g'],d['Temp'],d['Pressure'],d['Altitude'],d['Sealevel_Pressure']))
        # value = HistoryValue(temperature=d['t'], humidity=d['h'],shidu=d['s'],guangzhao=d['g'],Temp=d['Temp'],Pressure=d['Pressure'],Altitude=d['Altitude'],Sealevel_Pressure= d['Sealevel_Pressure'])
        # value.save()
        settings.CURRENT_TEMPERATURE = d['t']
        settings.CURRENT_HUMIDITY = d['h']
        settings.CURRENT_SHIDU = d['s']
        settings.CURRENT_GUANGZHAO = d['g']
        settings.CURRENT_TEMP = d['Temp']
        settings.CURRENT_PRESSURE = d['Pressure']
        settings.CURRENT_ALTITUDE = d['Altitude']
        settings.CURRENT_SEALEVEL_PRESSURE = d['Sealevel_Pressure']
        settings.CURRENT_DATA = d['rade_data']

    if 'get' in request.GET:
        rts.get("http://192.168.43.210:5000" + "?op=" + request.GET['get'])
    if 'note' in request.GET:
        rts.get("http://192.168.43.210:5000" + "?op=" + "write" + "?note=" + request.GET['note'])
    if 'recv' in request.GET:
        t, h, s, g, Temp , Pressure , Altitude ,Sealevel_Pressure , rade_data = getValue()
        return HttpResponse(json.dumps({'t': t, 'h': h, 's': s, 'g' : g,"Temp" : Temp,"Pressure" : Pressure,"Altitude" : Altitude,"Sealevel_Pressure" : Sealevel_Pressure , "rade_data" : rade_data}))
    return HttpResponse("ok")
