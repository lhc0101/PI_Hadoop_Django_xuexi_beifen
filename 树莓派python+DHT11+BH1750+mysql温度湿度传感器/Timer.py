# -*- coding: utf-8 -*-
#encoding: utf-8
import threading
import time
import os
import gc
import sys
sys.path.append('Library')
from Logger import *  ##打印日志输出函数

"""
    Created on 2017年7月17日
    @author: 定时任务
"""

###调用log方法
ptimee = time.strftime("%Y-%m-%d", time.localtime())
tfile = r'logs/sensor'+ptimee+'.log'
logger = Logger(logname=tfile, loglevel=1, logger="person timer:::").getlog()

class Person(object):
    def __init__(self):
        logger.info("init person")
        
    def speak(self):
        logger.info("speak 001")
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        ###整点运行
        ##logger.info("sh /home/pi/ST/hwclock/wu.sh")
        ##os.system("sh /home/pi/ST/hwclock/wu.sh")

class Person2(object):
    def __init__(self):
        logger.info("init person 2")
        
    def speak(self):
        logger.info("speak 002")
        logger.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logger.info("python3 sensor_nolog.py")
        os.system("python3 sensor.py")        

if __name__ == "__main__":
    p = Person()
    p2 = Person2()
    while True:
        time_mm = time.strftime("%M%S", time.localtime())
        if int(time_mm)>= 1101 and int(time_mm)<= 1109 :
            logger.info("==========1100==1109=========")
            timer = threading.Timer(10, Person2.speak, (p2,))
            timer.start()
            timer.join()
        if int(time_mm)>= 2001 and int(time_mm)<= 2009 :
            logger.info("==========2001==2009=========")
            timer = threading.Timer(10, Person2.speak, (p2,))
            timer.start()
            timer.join()            
        if int(time_mm)>= 3001 and int(time_mm)<= 3009 :
            logger.info("==========3000==3009=========")
            timer = threading.Timer(10, Person2.speak, (p2,))
            timer.start()
            timer.join()
        if int(time_mm)>= 4001 and int(time_mm)<= 4009 :
            logger.info("==========4000==4009=========")
            timer = threading.Timer(10, Person2.speak, (p2,))
            timer.start()
            timer.join()
        if int(time_mm)>= 0 and int(time_mm)<= 2 :
            logger.info("==========0001==0004====00:00=====")
            timer = threading.Timer(4, Person.speak, (p,))
            timer.start()
            timer.join()
        del time_mm
        gc.collect()
