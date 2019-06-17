import RPi.GPIO 
import time 
import datetime 

GPIOVIBRATE=20

GPIO_LED=11
SLEEPSECOND=0.5
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_VIBRATE,RPi.GPIO.IN)
RPi.GPIO.setup(GPIO_LED,RPi.GPIO.OUT)
while True: 
	print("time:"+str(datetime.datetime.now()))
	light=RPi.GPIO.input(GPIO_VIBRATE)
	print("Get message from GPIO vibrate %d"% light)
	if light>0: 
		RPi.GPIO.output(GPIO_LED, RPi.GPIO.HIGH)
		print("vibrate detected, open the LED")
	else: 
		RPi.GPIO.output(GPIO_LED, RPi.GPIO.LOW)
		print("no vibrate, close the LED")
	time.sleep(SLEEP_SECOND)