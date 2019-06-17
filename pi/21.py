import smbus
import time
import thread
import requests
from flask import Flask, request

REMOTE_SERVER_URL = "http://192.168.137.15:8000/data"

GPIO_LED = 11
 
RPi.GPIO.setup(GPIO_LED, RPi.GPIO.OUT)

bus=smbus.SMBus(1)
app = Flask(__name__)
def setup(Addr):
    global address
    address = Addr

def read(chn): 
    if chn == 0:
        bus.write_byte(address,0x40)
    if chn == 1:
        bus.write_byte(address,0x41)
    if chn == 2:
        bus.write_byte(address,0x42)
    if chn == 3:
        bus.write_byte(address,0x43)
    bus.read_byte(address) 
    return bus.read_byte(address)

def write(val):
    temp = val 
    temp = int(temp) 
    bus.write_byte_data(address, 0x40, temp)

def getValue(name,value):
    global LED_OPENED
    setup(0x48)
    while LED_OPENED:
        data1 = read(1)
        if data1 != None:
            send_data = {"c":data1}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            print("time: " + str(datetime.datetime.now()))
            print("send {0}".format(send_data))
        time.sleep(0.2)

@app.route('/', methods=['GET'])
def index():
    global LED_OPENED
    if 'op' in request.args:
        if request.args['op'] == "on" and not LED_OPENED:
            
            LED_OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))

        elif request.args['op'] == "off" and LED_OPENED:
            
            LED_OPENED = False
    return 'ok'

app.run(host='0.0.0.0')


