#coding=utf-8

import time

import requests

from Util import *
from base.base import HttpBase,HuobiBase

class HuobiSpot:
    def __init__(self, vp_ApiKey, vp_SecretKey, vp_BaseUrl):
        self.__ApiKey = vp_ApiKey
        self.__SecretKey = vp_SecretKey
        self.__BaseUrl = vp_BaseUrl
        self.__HuobiBase = HuobiBase()
        
    '''
    获取账号详情
    '''
    # 获取用户账户信息
    def getAccountInfo(self): 
        params = {}

        request_path = ACCOUNTS
        return self.__HuobiBase.api_key_get(self.__BaseUrl, request_path, params, self.__ApiKey, self.__SecretKey)


