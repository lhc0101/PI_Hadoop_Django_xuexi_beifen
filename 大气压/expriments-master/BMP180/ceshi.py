import requests
import RPi.GPIO
import time
import datetime
from flask import Flask, request
import thread

import Adafruit_BMP.BMP085 as BMP085

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rc522

sensor = BMP085.BMP085()



GPIO_DHT11 = 21
GPIO_LED = 26
SLEEP_SECOND = 2
turang = 20
guang = 16

LED_OPENED = False


REMOTE_SERVER_URL = "http://192.168.43.46:8000/data"

data2 = None



app = Flask(__name__)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_LED, RPi.GPIO.OUT)
RPi.GPIO.setup(turang, RPi.GPIO.IN)
RPi.GPIO.setup(guang, RPi.GPIO.IN)

# def a():

    # while True:
   
        # if GPIO.input(turang) == GPIO.LOW:
            # shidu = 0
        # else:
            # shidu = 1
        # time.sleep(1)


def getValue(name, value):
    global LED_OPENED
    while LED_OPENED:
        Temp = format(sensor.read_temperature())
        Pressure = format(sensor.read_pressure())
        Altitude = format(sensor.read_altitude())
        Sealevel_Pressure = format(sensor.read_sealevel_pressure())
        if Temp != None:
            # send_data = {"s":shidu}
            send_data = {"Temp":Temp,"Pressure":Pressure,"Altitude":Altitude,"Sealevel_Pressure":Sealevel_Pressure,"rade_data":Sealevel_Pressure}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            # print("time: " + str(datetime.datetime.now()))
            print("time: 2019-05-12 15:30")
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)

@app.route('/', methods=['GET'])
def index():
    global LED_OPENED
    if 'op' in request.args:
        if request.args['op'] == "on" and not LED_OPENED:
            RPi.GPIO.output(GPIO_LED, RPi.GPIO.HIGH)
            LED_OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))

        elif request.args['op'] == "off" and LED_OPENED:
            RPi.GPIO.output(GPIO_LED, RPi.GPIO.LOW)
            LED_OPENED = False
        elif request.args['op'] == "read":
            rade_data()
            
    return 'ok'

app.run(host='0.0.0.0')

