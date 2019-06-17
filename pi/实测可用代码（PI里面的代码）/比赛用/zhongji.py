import requests
import RPi.GPIO
import time
import datetime
from flask import Flask, request
import thread

import smbus
import time

GPIO_DHT11 = 4
GPIO_jiaoshui = 17
GPIO_shifei = 27
SLEEP_SECOND = 2
# turang = 21 
# guang = 16

shebeiid = 100001

OPENED = False
# REMOTE_SERVER_URL = "http://118.25.142.54:8000/data"
# REMOTE_SERVER_URL_api = "http://192.168.43.46:8000/api/v1.0/service/stock"
REMOTE_SERVER_URL_api = "http://192.168.43.46:8000/data"
# REMOTE_SERVER_URL = "http://192.168.43.208:8000/data"



app = Flask(__name__)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_jiaoshui, RPi.GPIO.OUT)
RPi.GPIO.setup(GPIO_shifei, RPi.GPIO.OUT)
# RPi.GPIO.setup(turang, RPi.GPIO.IN)
# RPi.GPIO.setup(guang, RPi.GPIO.IN)

# def a():

    # while True:
   
        # if GPIO.input(turang) == GPIO.LOW:
            # shidu = 0
        # else:
            # shidu = 1
        # time.sleep(1)


# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

#check your PCF8591 address by type in 'sudo i2cdetect -y -1' in terminal.
def setup(Addr):
    global address
    address = Addr

def read(chn): #channel
    if chn == 0:
        bus.write_byte(address,0x40)
    if chn == 1:
        bus.write_byte(address,0x41)
    if chn == 2:
        bus.write_byte(address,0x42)
    if chn == 3:
        bus.write_byte(address,0x43)
    bus.read_byte(address) # dummy read to start conversion
    return bus.read_byte(address)

def write(val):
    temp = val # move string value to temp
    temp = int(temp) # change string to integer
    # print temp to see on terminal else comment out
    bus.write_byte_data(address, 0x40, temp)        


def setupDHT11():
    RPi.GPIO.setup(GPIO_DHT11, RPi.GPIO.OUT)
    RPi.GPIO.output(GPIO_DHT11, RPi.GPIO.LOW)
    time.sleep(0.02)
    RPi.GPIO.output(GPIO_DHT11, RPi.GPIO.HIGH)
    RPi.GPIO.setup(GPIO_DHT11, RPi.GPIO.IN)

def DHT11read():
    data = []
    while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.LOW:
        continue
    while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.HIGH:
        continue
    j = 0
    while j < 40:
        k = 0
        while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.LOW:
            continue
        while RPi.GPIO.input(GPIO_DHT11) == RPi.GPIO.HIGH:
            k += 1
            if k > 100:
                break
        if k < 8:
            data.append(0)
        else:
            data.append(1)
        j += 1
    return data

def checkData(data):
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]
    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0
    for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7-i)
        humidity_point += humidity_point_bit[i] * 2 ** (7-i)
        temperature += temperature_bit[i] * 2 ** (7-i)
        temperature_point += temperature_point_bit[i] * 2 ** (7-i)
        check += check_bit[i] * 2 ** (7-i)
    tmp = humidity + humidity_point + temperature + temperature_point
    if check == tmp:
        print("temperature :{0} C, humidity :{1} %%".format(temperature, humidity))
        return temperature, humidity
    else:
        print("got wrong data now")
    return None, None

def getValue(name, value):
    global OPENED
    setup(0x48)
    while OPENED:
        print 'AIN0 = ', read(0)
        print 'AIN1 = ', read(1)
        print 'AIN2 = ', read(2)
        print 'AIN3 = ', read(3)
        tmp = read(0)
        tmp = tmp*(255-125)/255+125 # LED won't light up below 125, so convert '0-255' to '125-255'
        # write(tmp)
        print(tmp)
        time.sleep(1)
        setupDHT11()
        data = DHT11read()
        temperature, duoyushuju = checkData(data)
        shidu = read(2)
        guangzhao = tmp
        humidity = read(1)
        if temperature != None:
            send_data = {"t":temperature, "h":humidity,"s":shidu,"g":guangzhao,"id":shebeiid}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            # req = requests.post(REMOTE_SERVER_URL_api + "?data=" + str(send_data))
            print("time: " + str(datetime.datetime.now()))
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)

@app.route('/', methods=['GET'])
def index():
    global OPENED
    if 'op' in request.args:
        if request.args['op'] == "on" and not OPENED:
            OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))

        elif request.args['op'] == "off" and OPENED:
            OPENED = False

        elif request.args['op'] == "on-water":
            RPi.GPIO.output(GPIO_jiaoshui, RPi.GPIO.HIGH)
            # OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))
            time.sleep(1)
            RPi.GPIO.output(GPIO_jiaoshui, RPi.GPIO.LOW)

        elif request.args['op'] == "off-water" and OPENED:
            RPi.GPIO.output(GPIO_jiaoshui, RPi.GPIO.LOW)
            # OPENED = False

        elif request.args['op'] == "on-shifei":
            RPi.GPIO.output(GPIO_shifei, RPi.GPIO.HIGH)
            # OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))
            time.sleep(1)
            RPi.GPIO.output(GPIO_shifei, RPi.GPIO.LOW)

        elif request.args['op'] == "off-shifei" and OPENED:
            RPi.GPIO.output(GPIO_shifei, RPi.GPIO.LOW)
            # OPENED = False
    return 'ok'

app.run(host='0.0.0.0',port=5001)

