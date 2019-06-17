# -*- coding: utf-8 -*-
#encoding: utf-8

from si7021 import Si7021
from time import sleep
from smbus import SMBus
sensor = Si7021(SMBus(1))
print(sensor.read())
sensor.heater_mA = 50
sleep(10)
print(sensor.read())
sensor.heater_mA = 0
