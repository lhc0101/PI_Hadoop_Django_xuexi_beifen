# -*- coding: utf-8 -*-
#encoding: utf-8

"""
    @pip3 install pygame
    @pip3 install configparser
    @pip3 install Jinja2
    @pip3 install Flask
"""
import sys
import json
import time
import uuid
import hashlib
import gc
import os
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from flask import render_template
#from flask.ext.bootstrap import Bootstrap
sys.path.append('Library')
import ConfigParser
from MySQLdbDB_Util_py3 import *
from DateUtil_py3 import *
from Logger import *
from base_CV import *  ##base64函数

Specificdate = time.strftime("%Y-%m-%d", time.localtime())
files = r'logs/server_sys'+Specificdate+'.log'
logger = Logger(logname=files, loglevel=1, logger="-").getlog()

#bootstrap=Bootstrap(app)
app = Flask(__name__, static_url_path='')
##server.conf 参数
cpo = ConfigParser.SafeConfigParser()
with open("server.conf", "r",encoding="utf-8") as f:
    cpo.readfp(f)
server_host = cpo.get("sor_server", "server_json_host")
server_port = cpo.get("sor_server", "server_json_port")

logger.info (server_host)

##异常页面处理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('404.html'),500


@app.route('/' , methods=['GET', 'POST'])
def root():
    #return render_template('index.html')
    return app.send_static_file('index.html')

@app.route('/sys.do' , methods=['GET', 'POST'])
def root_001():
    return render_template('sys.html')

@app.route('/sysreboot.do' , methods=['GET', 'POST'])
def root_002():
    host = request.url_root
    logger.info (host)
    if request.method == 'POST':

        #os.system("dir")
        
        process = os.popen('sudo reboot') # return file
        output = process.read()
        response = "<html>\n"
        print (output)
        response += output
        response += "</html>\n"
        process.close()
        #return render_template('sysreboot.html')
        return response
    else:
        response = "<html>\n"
        response += "<title>WEB system API</title>\n"
        response += "<body>\n"
        response += "<h1>POST data\n</h1>"
        response += "访问来源："+host+""
        response += "</body>\n"
        response += "</html>\n"

        return response
    gc.collect()

@app.route('/syshalt.do' , methods=['GET', 'POST'])
def root_003():
    host = request.url_root
    logger.info (host)
    if request.method == 'POST':

        #os.system("dir")        
        response = "<html>\n"
        process = os.popen('sudo halt') # return file
        output = process.read()
        print (output)
        response += output
        response += "</html>\n"
        process.close()
        #return render_template('sysreboot.html')
        return response
    else:
        response = "<html>\n"
        response += "<title>WEB system API</title>\n"
        response += "<body>\n"
        response += "<h1>POST data\n</h1>"
        response += "访问来源："+host+""
        response += "</body>\n"
        response += "</html>\n"

        return response
    gc.collect()    


if __name__ =='__main__':
    app.run(host = "0.0.0.0",port = int(server_port),debug = True)
    
