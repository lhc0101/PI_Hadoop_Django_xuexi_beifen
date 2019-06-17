#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time
import datetime 

channel = 21 #管脚40，参阅树莓派引脚图，物理引脚40对应的BCM编码为21

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

        
while True:
    light = GPIO.input(channel)
    if light == GPIO.LOW:
        shidu = "潮湿"
    else:
        shidu = "干燥"
    print ("time:"+str(datetime. datetime. now()))
    if light == GPIO.LOW:
        print shidu
    else:
        print shidu
    time.sleep(1)