import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rc522

reader = rc522()
door = 7
READ = 0
WRITE = 1
operation = READ

GPIO.setup(door, GPIO.OUT)
door = False
def rade_data():
    try: 
        print("begin reading")
        id, data=reader.read()
    except Exception as error: 
        print("error happened:"+str(error))
    finally: 
        GPIO.cleanup()
    return id,data

def write_data():    
    try: 
        data=raw_input("input data:") 
        print("input data is:"+ data)
        print("place your card to write")
        reader.write(data)
        print("write success")
    except Exception as error: 
        print("error happened:"+str(error))
    finally: 
        GPIO.cleanup()
    return ok


def getValue(name, value):
    global door
    while door:
        id1,data1 = rade_data()
        print(id1)
        if id1!= None:
            # send_data = {"s":shidu}
            send_data = {"id":"{}".format(id1), "data":"{}".format(data1) }
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            # print("time: " + str(datetime.datetime.now()))
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)

@app.route('/', methods=['GET'])
def def index():
    global door
    if 'op' in request.args:
        if request.args['op'] == "on" and not door:
            RPi.GPIO.output(GPIO_LED, RPi.GPIO.HIGH)
            door = True
            thread.start_new_thread(getValue, ("getValue", None))

        elif request.args['op'] == "off" and door:
            RPi.GPIO.output(GPIO_LED, RPi.GPIO.LOW)
            door = False
    return 'ok'

app.run(host='0.0.0.0')
