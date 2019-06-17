import RPi.GPIO as RG
import time as t
import datetime

GPIO_MOTOR = 20
GPIO_LED = 11
SLEEP_SECOND = 2
FREQUENCE = 50 # Hz

RG.setmode(RG.BCM)
RG.setup(GPIO_LED,RG.OUT)

MOVE_STEP = 20
RG.setup(GPIO_MOTOR,RG.OUT)
pulse = RG.PWM(GPIO_MOTOR,FREQUENCE)
pulse.start(0)
t.sleep(2)

while True:
	print("time:" + str(datetime.datetime.now()))

	RG.output(GPIO_LED,RG.HIGH)
	print("Motor start,open the LED")
	for i in range(MOVE_STEP):
		pulse.ChangeDutyCycle(2.5 + i * 10.0 / MOVE_STEP)
		t.sleep(1.0 / FREQUENCE)
	RG.output(GPIO_LED,RG.LOW)
	print("Motor stop,close the LED")
	t.sleep(SLEEP_SECOND)

	RG.output(GPIO_LED,RG.HIGH)
	print("Motor start,open the LED")
	for i in range(MOVE_STEP):
		pulse.ChangeDutyCycle(2.5 + (MOVE_STEP - i) * 10.0 / MOVE_STEP)
		t.sleep(1.0 / FREQUENCE)
	RG.output(GPIO_LED,RG.LOW)
	print("Motor stop,close the LED")
	t.sleep(SLEEP_SECOND)
	