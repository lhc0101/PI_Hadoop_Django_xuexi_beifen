import requests
import RPi.GPIO
import time
import datetime
from flask import Flask, request
import thread


import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rc522





GPIO_DHT11 = 21
GPIO_LED = 26
SLEEP_SECOND = 2
turang = 20
guang = 16

LED_OPENED = False
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_LED, RPi.GPIO.OUT)

REMOTE_SERVER_URL = "http://192.168.43.46:8000/data"

data2 = None

reader = rc522()

app = Flask(__name__)

# def a():

    # while True:
   
        # if GPIO.input(turang) == GPIO.LOW:
            # shidu = 0
        # else:
            # shidu = 1
        # time.sleep(1)

def rade_data():
    try: 
        print("begin reading")
        id, data=reader.read()
    except Exception as error: 
        print("error happened:"+str(error))
    finally: 
        GPIO.cleanup()
    return id,data

def getValue(name, value):
    global LED_OPENED
    while LED_OPENED:
        id1,data1 = rade_data()
        print(data1)
        if data1 != None:
            # send_data = {"s":shidu}
            send_data = {"ID":id1,"data":data1.split()}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            # print("time: " + str(datetime.datetime.now()))
            print("time: 2019-05-12 15:24")
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)



# def getValue(name, value):
#     global LED_OPENED
#     while LED_OPENED:
#         id1 = rade_data()
#         if id1 != None:
#             # send_data = {"s":shidu}
#             send_data = {"Altitude":0,"Sealevel_Pressure":0}
#             req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
#             print("time: " + str(datetime.datetime.now()))
#             print("send {0}".format(send_data))
#         time.sleep(SLEEP_SECOND)

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
            
    return 'ok'

app.run(host='0.0.0.0')

