import requests
import RPi.GPIO
import time
import datetime
from flask import Flask, request
import thread



GPIO_DHT11 = 21
GPIO_LED = 26
SLEEP_SECOND = 2
turang = 20
guang = 16

LED_OPENED = False
REMOTE_SERVER_URL = "http://192.168.43.46:8000/data"



app = Flask(__name__)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_LED, RPi.GPIO.OUT)
RPi.GPIO.setup(turang, RPi.GPIO.IN)
RPi.GPIO.setup(guang, RPi.GPIO.IN)


def getValue(name, value):
    global LED_OPENED
    while LED_OPENED:
        shidu = RPi.GPIO.input(turang)
        guangzhao = RPi.GPIO.input(guang)
        if shidu != None:
            send_data = {"t":shidu}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            print("time: " + str(datetime.datetime.now()))
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
    return 'ok'

app.run(host='0.0.0.0')

