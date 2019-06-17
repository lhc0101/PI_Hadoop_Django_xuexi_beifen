# -*- coding: utf-8 -*-
#!/usr/bin/python
import RPi.GPIO as GPIO
import os
import sys
import socket
import subprocess
import time

"""
    $Explain
    @$humiture DHT11 温度湿度采集
    @接口地址 GPI接口地址23,BCM编码格式
    @date 2017-07-18
"""

def get_Humiture():
    channel = 23 ##GPI23
    data = []
    j = 0

    GPIO.setmode(GPIO.BCM) ##以BCM编码格式  
    time.sleep(1)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(channel, GPIO.HIGH)
    GPIO.setup(channel, GPIO.IN)

    while GPIO.input(channel) == GPIO.LOW:
        continue

    while GPIO.input(channel) == GPIO.HIGH:
        continue

    while j < 40:
        k = 0
        while GPIO.input(channel) == GPIO.LOW:
            continue
    
        while GPIO.input(channel) == GPIO.HIGH:
            k += 1
            if k > 100:
                break
    
        if k < 8:
            data.append(0)
        else:
            data.append(1)

        j += 1

    print ("正在访问温度湿度传感器数据.GPIO",channel)
    
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
        humidity += humidity_bit[i] * 2 ** (7 - i)
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
        temperature += temperature_bit[i] * 2 ** (7 - i)
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
        check += check_bit[i] * 2 ** (7 - i)

    tmp = humidity + humidity_point + temperature + temperature_point

    if check == tmp:                                #数据校验，相等则输出  
        print ("温度湿度传感器数据 | 温度 : ", temperature, "*C, 湿度 : " , humidity, "%")
        return (temperature,humidity)
    
    else:                                       #错误输出错误信息，和校验数据  
        print ("wrong")
        print ("temperature : ", temperature, ", humidity : " , humidity, " check : ", check, " tmp : ", tmp)
        _temperature = '00'
        _check = '00'
        return (_temperature,_check)   

    GPIO.cleanup()
