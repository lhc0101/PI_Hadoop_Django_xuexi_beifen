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


reader = rc522()

def rade_data():
    try:
        print("begin reading")
        id1, data1 = reader.read()
        # print("id is: "+str(id1))
        # print("data is: "+str(data1))
        print("id is"+str(id))
        print("data is"+str(data)) 
        print("time: " + str(datetime.datetime.now()))
        print("send {0}".format(send_data))

    except Exception as error:
        print("error happened:"+str(error))
                        
    finally:
        GPIO.cleanup()


def write_data():
    try:
        # data2=raw_input('input data:')
        print( 'input data is:'+ data2)
        print( "place your card to write")
        reader.write(data2)
        print( "write success")

    except Exception as error:
        print( "error happened:"+ str (error ))
    finally:
        GPIO.cleanup()


def setupDHT11():
    RPi.GPIO.setup(GPIO_DHT11, RPi.GPIO.OUT)
    RPi.GPIO.output(GPIO_DHT11, RPi.GPIO.LOW)
    time.sleep(0.02)
    RPi.GPIO.output(GPIO_DHT11, RPi.GPIO.HIGH)
    RPi.GPIO.setup(GPIO_DHT11, RPi.GPIO.IN)

def read():
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
    global LED_OPENED
    while LED_OPENED:
        setupDHT11()
        data = read()
        temperature, humidity = checkData(data)
        shidu = RPi.GPIO.input(turang)
        guangzhao = RPi.GPIO.input(guang)
        print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
        print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
        print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
        print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
        Temp = format(sensor.read_temperature())
        Pressure = format(sensor.read_pressure())
        Altitude = format(sensor.read_altitude())
        Sealevel_Pressure = format(sensor.read_sealevel_pressure())
        if temperature != None:
            send_data = {"t":temperature, "h":humidity,"s":shidu,"g":guangzhao,"Temp":Temp,"Pressure":Pressure,"Altitude":Altitude,"Sealevel_Pressure":Sealevel_Pressure}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            print("time: " + str(datetime.datetime.now()))
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)

@app.route('/', methods=['GET'])
def index():
    global LED_OPENED
    global data2
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
        elif request.args['op'] == "write":
            data2 = request.args['note']
            write_data()
            
    return 'ok'

app.run(host='0.0.0.0')

