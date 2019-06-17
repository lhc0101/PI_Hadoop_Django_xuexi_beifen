# -*- coding:utf-8 -*-
# coding=utf-8
import sys
import os
import re
import socket

###判断端口是否打开
###IsOpen('127.0.0.1',13306)
def IsOpen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        #print '%d is open' % port
        return True
    except:
        #print '%d is down' % port
        return False

def get_weather_url_data(city_name):
    city={
    "广州":"101280101",
    "北京":"101010100",
    "上海":"101020100",
    "张家界":"101251101",
    "慈利":"101251103",
    "岳阳":"101251001",
    "益阳":"101250700",
    "常德":"101250601",
    "怀化":"101251201",
    "长沙":"101250101"
    }
    #for k in city:
    #    print(k)
    #city_name=input("请输入你要查询的城市名字：")
    #city_name= "长沙"
    city_num=city[city_name]
    weather_url="http://www.weather.com.cn/weather/%s.shtml"%city_num
    return weather_url

def get_Gis_data(city_name):
    city={
    "广州":"113.1553′E,23.0632′N",
    "北京":"116.2529′E,39.5420′N",
    "上海":"120.52′E,30.40′N",
    "张家界":"109.40′E,25.52′N",
    "慈利":"110.27′E,29.04′N",
    "岳阳":" ′E, ′N",
    "益阳":" ′E, ′N",
    "常德":" ′E, ′N",
    "怀化":" ′E, ′N",
    "长沙":"112.5842′E,28.1149′N"
    }
    #for k in city:
    #    print(k)
    city_gis=city[city_name]
    return city_gis

#if __name__=="__main__":
    # url="http://www.weather.com.cn/weather/101190401.shtml"
#    _city_name = "长沙"
#    url=get_weather_url_data(_city_name)
#    gis_url=get_Gis_data(_city_name)
#    print(url)
#    print(gis_url)
