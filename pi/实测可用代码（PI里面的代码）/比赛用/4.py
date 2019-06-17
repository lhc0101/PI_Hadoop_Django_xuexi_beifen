import RPi.GPIO 
import time 
import datetime 

GPIO_HUMAN=20
GPIO_LED=11

SLEEP_SECOND=0.5
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_HUMAN,RPi.GPIO.IN)
RPi.GPIO.setup(GPIO_LED,RPi.GPIO.OUT)

while True: 
	print("time:"+str(datetime. datetime. now()))
	light =RPi. GPIO. input(GPIO_HUMAN)
	print("Get message from GPIO human %d"% light)
	if light>0: 
		RPi.GPIO.output(GPIO_LED,RPi.GPIO.HIGH)
		print("human detected, open the LED")
	else: 
		RPi.GPIO.output(GPIO_LED, RPi.GPIO.LOW)
		print("nobody here, close the LED")
	time.sleep(SLEEP_SECOND)