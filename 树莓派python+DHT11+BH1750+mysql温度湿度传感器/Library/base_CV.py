# -*- coding: utf-8 -*-
#encoding: utf-8
import base64
import hashlib

#@base64编码
def Base_mpd(_mgc):
    #转成bytes string
    bytesString = _mgc.encode(encoding="utf-8")
    #base64 编码
    encodestr = base64.b64encode(bytesString)
    #print("001",encodestr)
    #print("002",encodestr.decode())
    return encodestr,encodestr.decode()

#@base64编码 单值
def Base_mpd_in(_mgc):
    #转成bytes string
    bytesString = _mgc.encode(encoding="utf-8")
    #base64 编码
    encodestr = base64.b64encode(bytesString)
    #print("001",encodestr)
    #print("002",encodestr.decode())
    return encodestr

#@base64解码 单值
def Base_mp_in(_iou):
    #Base64解析信息
    decodestr = base64.b64decode(_iou)
    print("Base64解析信息 单个操作：",decodestr.decode())
    return decodestr.decode()

#@base64解码
def Base_mp(_iou):
    #Base64解析信息
    _iou_1 = _iou[0]
    decodestr = base64.b64decode(_iou_1)
    print("Base64解析信息：",decodestr.decode())
    return decodestr.decode()
    
def str_encrypt(str):
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(str)
    encrypts = sha.hexdigest()
    return encrypts