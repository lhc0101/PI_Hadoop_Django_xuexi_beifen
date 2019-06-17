# -*- coding: utf-8 -*-
#encoding: utf-8
""" 
    @author: 
    @version: 2017-06-29
    @封装的mysql常用函数
    pip3 install PyMySQL

""" 
import pymysql.cursors
import socket
import ConfigParser

class DB():
    
    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PWD, DB_NAME):
        
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT
        self.DB_USER = DB_USER
        self.DB_PWD = DB_PWD
        self.DB_NAME = DB_NAME
        self.conn = self.getConnection()

    def getConnection(self):

        return pymysql.connect(            
            host = self.DB_HOST, #设置MYSQL地址
            port = self.DB_PORT, #设置端口号
            user = self.DB_USER, #设置用户名
            passwd = self.DB_PWD, #设置密码
            db = self.DB_NAME, #数据库名
            charset = 'utf8' #设置编码
        )

    def query(self, sqlString):
        
        cursor = self.conn.cursor()
        cursor.execute(sqlString)
        returnData = cursor.fetchall()
        cursor.close()
        self.conn.close()

        return returnData
        
    def query_cd(self, sqlString):
        
        cursor = self.conn.cursor()
        cursor.execute(sqlString)
        returnData = cursor.fetchone()
        cursor.close()
        self.conn.close()

        return returnData

    def update(self, sqlString):

        cursor = self.conn.cursor()
        cursor.execute(sqlString)
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def insert(self, sqlString):

        cursor = self.conn.cursor()
        cursor.execute(sqlString)
        self.conn.commit()
        cursor.close()
        self.conn.close()

"""         
def getby_mysql_host(_CIP):
    host={
    "1":"127.0.0.1",
    "2":"192.168.20.135",
    "3":"192.168.20.129"
    }
    _host=host[_CIP]
    #print "MySQLdb.connect IP:",_host
    return _host
       
def getby_mysql_config():
    db_user = 'root'
    db_password = 'bigdata@2016'
    db_schema = 'com_it'
    db_port = 13306
    db_host = getby_mysql_host("1")
    #db_host = '192.168.20.135'
    db2=DB(db_host ,db_port ,db_user ,db_password ,db_schema )
    return db2
"""

def getby_mysql_config():
    cp = ConfigParser.SafeConfigParser()
    #with codecs.open('jdbc.conf', 'r', encoding='utf8') as f:  ##python2
    with open('jdbc.conf', 'r') as f:  ##python3
        cp.readfp(f)
    db_user = str(cp.get('dbs', 'db_user'))
    db_password = str(cp.get('dbs', 'db_password'))
    db_schema = str(cp.get('dbs', 'db_schema'))
    db_port = int(cp.get('dbs', 'db_port'))
    db_host = str(cp.get('dbs', 'db_host'))
    #print ("host:",db_host)
    #db=DB('127.0.0.1',13306,'root','bigdata@2016','com_it')
    db2=DB(db_host ,db_port ,db_user ,db_password ,db_schema )
    return db2

#if __name__=="__main__":
#    getby_mysql_config()
