# -*- coding: utf-8 -*-
#encoding: utf-8
import os
import json
import gc
import sys
sys.path.append('Library') #添加自定义包
from Logger import *  ##打印日志输出函数
from DateUtil_py3 import *  ##时间常用输出字典函数
from MySQLdbDB_Util_py3 import *  ##mysql函数
from data_ini import *  ##自定义字典函数
from DHT11_ini import * ##温度湿度传感器
from iic_bh1750_gy30ini import * ##光照强度传感器
        
"""
    $Explain
    @ import datetime
    @ import time
    @ pip3 install urllib
"""

#调用log方法
ptimee = time.strftime("%Y-%m-%d", time.localtime())
tfile = r'logs/sensor'+ptimee+'.log'
logger = Logger(logname=tfile, loglevel=1, logger="by_humiture_sensor:::").getlog()

##########################################
######%Y-%m-%d %H:%M:%S 月 日 小时      
t_str_01 = time.strftime('%Y-%m',time.localtime(time.time()))
t_str_m = time.strftime('%m',time.localtime(time.time()))
t_str_d = time.strftime('%d',time.localtime(time.time()))
t_str_H = time.strftime('%H',time.localtime(time.time()))
t_str_mm = time.strftime('%M',time.localtime(time.time()))
t_str_Hh = "h" + t_str_H
d_io=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
d_ioioymd=time.strftime('%Y%m%d',time.localtime(time.time()))
print ("%Y-%m-%d %H:%M:%S:::",t_str_m,t_str_d,t_str_Hh,d_ioioymd)

def store(temperature ,humidity ,lux):
    ##json
    data = {}
    data["date"]=d_io
    data["temperature"]= temperature
    data["humidity"]= humidity
    data["lx"]= lux
    ##写入文件
    f = open('datas/data.json', 'w')
    ioc = json.dumps(data)       
    logger.info(ioc)
    f.write(ioc)
    f.close()
                
"""
    $Explain
    by_humiture_sensor 查询数据每小时记录是否存在
    by_humiture_sensor 创建一条小时记录数据
    by_humiture_sensor 创建一条执行时间小时内记录数据
    @date 2017-07-15
"""
def getby_humiture_cu(_day_dic ,_day_dic_w ,add_name_id ,t_mm):
        logger.info("getby_humiture_cu ")        
        
        try:                
                #############by_humiture
                sqlq = 'SELECT * FROM by_humiture_sensor WHERE t_hm ='"%s"' AND t_hD='"%s"' AND t_hH='"%s"' AND t_mm='"%s"';'\
                % (t_str_m ,t_str_d ,t_str_H ,t_mm)
                print ("查询是否存在记录 by_humiture_sensor：",t_str_m ,t_str_d ,t_str_H,t_mm )
                logger.info("getby_humiture_cu by_humiture_sensor Doces the record exist? t_hm ,t_hd ,t_hH ,t_mm")
                count_1 = getby_mysql_config().query_cd(sqlq)
                logger.info(count_1)
                #print (count_1)
                if not count_1 or count_1 == 0:
                        sqlw = 'INSERT INTO by_humiture_sensor (t_dict, t_dictweek ,t_time,t_hm,t_hD,t_hH,t_mm,G_temperature,G_humidity,add_name_id) \
                                VALUES ("%s","%s" ,now(),''"%s"'',''"%s"'',''"%s"'',''"%s"'',"00","00",''"%s"'');' % (_day_dic ,_day_dic_w ,t_str_m ,t_str_d ,t_str_H ,t_mm,add_name_id)                               
                        getby_mysql_config().insert(sqlw)
                        #print (sqlw)
                        logger.info("by_humiture_sensor  创建新记录")
                
        except Exception as e: 
            logger.info("getby_humiture_cu Mysql Error ")
            logger.info(e)

        return True

"""
    by_humiture写入每小时记录
    by_humiture_baidu/by_humiture 更新一条执行时间小时内记录数据
    @date 2017-06-28
"""
def getby_humiture_in(_temperature,_humidity ,_gis_url ,add_name_id ,hio ,t_mm ,lux):
        logger.info("getby_humiture_in ")
        """
            #debug
            #from DHT11_ini import * ##温度湿度传感器
            #from iic_bh1750_gy30ini import * ##光照强度传感器
            #$temperature = 21
            #$humidity = 91
            #$_GPIO_LX_lux = getIlluminance()
            #$GPIO_LX_lux = _GPIO_LX_lux.split(':')[-1].strip()
            #$GPIO_LX_lux = "2.00"
            #$city_longitude 经度
            #$city_latitude 纬度
        """
        _iop01 = _temperature
        _iop02 = _humidity
        gis_url=get_Gis_data(_gis_url)
        city_longitude = gis_url.split(',')[0]
        city_latitude = gis_url.split(',')[-1]

        _by_ = str(t_str_m) + str(t_str_d) + str(t_str_H) + "温度:"+ str(_temperature) + "湿度:"+str(_humidity)+"光照强度:"+str(lux)
        try:
                sqlq_iop = 'UPDATE `by_humiture_sensor` SET `t_time`=now(),`HIO`=''"%s"'',`G_temperature`=''"%s"'', `G_humidity`=''"%s"'', `G_Lx`=''"%s"'',`sensor_name` =''"%s"'',\
                        `city_longitude` =''"%s"'',`city_latitude` =''"%s"'' WHERE \
                        t_hm ='"%s"' AND t_hD='"%s"' AND t_hH='"%s"' AND t_mm='"%s"' AND add_name_id='"%s"';'% (hio ,_iop01 ,_iop02 ,lux ,_gis_url ,city_longitude ,city_latitude ,t_str_m ,t_str_d ,t_str_H ,t_mm ,add_name_id)
                getby_mysql_config().update(sqlq_iop)
                logger.info("室内温湿度数据更新到by_humiture_sensor-->success ok!")
                #logger.info(sqlq_iop)
                
        except Exception as e: 
            logger.info("getby_humiture_in Mysql Error ")
            print (e)

        return True

"""
    getby_humiture_cu(_day_dic ,_day_dic_w) ##创建数据库表
    getby_humiture_in(temperature ,humidity ,_gis_url) #更新数据库表记录
    getIlluminance() #光照强度读取
    @date 2017-06-28    
"""
def getrun_win():
        _day_dic = get_week_day_(datetime.datetime.now()) ##星期
        _day_dic_w = get_week_day_w(datetime.datetime.now()) ##星期 代码 
        """
            #debug
            #from DHT11_ini import * ##温度湿度传感器
            #from iic_bh1750_gy30ini import * ##光照强度传感器
            $temperature = 21
            $humidity = 91
        """
        ##temperature humidity lux仿真值
        #temperature = "21"
        #humidity = "91"
        #lux = "00.00"
        dht = get_Humiture()
        temperature = dht[0]
        humidity = dht[1]
        lux = getIlluminance() ##光照传感器
        
        _gis_url = "长沙"
        add_name_id = "00" #执行所有者
        hio = "1" #监测环境干扰:0-自然环境;1-空调或人工;2-仿真数据
        if int(t_str_mm) >=30 :
                t_mm = "1"
        else :
                t_mm = "0"
        
        if int(humidity) ==0 :
            
            logger.info("temperature ,humidity 异常! ")
            
        elif int(humidity) > 100 :
            logger.info("temperature ,humidity 超过常规值，数据抛弃! ")
        else :  
            getby_humiture_cu(_day_dic ,_day_dic_w ,add_name_id ,t_mm) ##创建数据库空表
            getby_humiture_in(temperature ,humidity ,_gis_url ,add_name_id ,hio ,t_mm ,lux) #更新数据库表记录
            #store(temperature ,humidity ,lux)  ##json文件写入
            
        gc.collect()
        
if __name__ == '__main__':     
        getrun_win()
        
        
               

