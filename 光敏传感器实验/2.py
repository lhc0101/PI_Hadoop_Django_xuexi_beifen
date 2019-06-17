import RPi.GPIO 
import time 
import datetime 

GPIO_LIGHT=2
GPIO_LED=11

SLEEP_SECOND=1

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_LIGHT,RPi.GPIO.IN)
RPi.GPIO.setup(GPIO_LED,RPi.GPIO.OUT)

while True:
	print("time:"+str(datetime.datetime.now()))
	light=RPi.GPIO.input(GPIO_LIGHT)
	print("Get message from GPIo light %d" % light)
	if light>0: 
		RPi.GPIO.output(GPIO_LED, RPi.GPIO.HIGH)
		print("Dark now, open the LED")
	else: RPi.GPIO.output(GPIO_LED, RPi.GPIO.LOW)
		print("Light now, close the LED")
	time. sleep(SLEEP_SECOND)