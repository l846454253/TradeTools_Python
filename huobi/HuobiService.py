#coding=utf-8

import time

import requests

from huobi.Util import *


class HuobiSpot:

    def __init__(self, vp_ApiKey, vp_SecretKey, vp_BaseUrl):
        self.uApiKey = vp_ApiKey
        self.uSecretKey = vp_SecretKey
        self.uBaseUrl = vp_BaseUrl
        
        self.logger = logging.getLogger("huobi-client")
    
    '''
    获取账号详情
    '''
    def getAccountInfo(vp_Method):
        vl_TimeStamp = long(time.time())
        vl_Params = {"access_key":self.uApiKey, "secret_key":self.uSecretKey, "created":vl_TimeStamp, "method":vp_Method}
        vl_Sign = signature(vl_Params)
        
        vl_Params['sign'] = vl_Sign
        del vl_Params['secret_key']

        vl_Payload = urllib.urlencode(vl_Params)
        
        self.logger.debug(vl_Payload)
        
        r = requests.post(self.uBaseUrl, params=vl_Payload)
        if r.status_code == 200:
            return r.json()
        else:
            return r.raise_for_status() 

    '''
    下单接口
    @param coinType
    @param price
    @param amount
    @param tradePassword
    @param tradeid
    @param method
    '''
    def buy(vp_CoinType, vp_Price, vp_Amount, vp_TradePassword, vp_TradeId, vp_Method):
        vl_TimeStamp = long(time.time())
        params = {"access_key":self.uApiKey, "secret_key":self.uSecretKey, 
                "created":vl_TimeStamp, "price":vp_Price, "coin_type":vp_CoinType, "amount":vp_Amount, "method":vp_Method}
        sign=signature(params)
        params['sign']=sign
        del params['secret_key']
        if tradePassword:
            params['trade_password']=tradePassword
        if tradeid:
            params['trade_id']=tradeid

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    '''
    提交市价单接口
    @param coinType
    @param amount
    @param tradePassword
    @param tradeid
    '''

    def buyMarket(coinType,amount,tradePassword,tradeid,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"amount":amount,"method":method}
        sign=signature(params)
        params['sign']=sign
        if tradePassword:
            params['trade_password']=tradePassword
        if tradeid:
            params['trade_id']=tradeid

        del params['secret_key']

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None


    '''
    撤销订单
    @param coinType
    @param id
    '''

    def cancelOrder(coinType,id,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"id":id,"method":method}
        sign=signature(params)
        params['sign']=sign
        del params['secret_key']

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    '''
    查询个人最新10条成交订单
    @param coinType
    '''
    def getNewDealOrders(coinType,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method}
        sign=signature(params)
        params['sign']=sign
        del params['secret_key']

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    '''
    根据trade_id查询oder_id
    @param coinType
    @param tradeid
    '''
    def getOrderIdByTradeId(coinType,tradeid,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method,"trade_id":tradeid}
        sign=signature(params)
        params['sign']=sign
        del params['secret_key']

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    '''
    获取所有正在进行的委托
    @param coinType
    '''
    def getOrders(coinType,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method}
        sign=signature(params)
        params['sign']=sign
        del params['secret_key']

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    '''
    获取订单详情
    @param coinType
    @param id
    '''
    def getOrderInfo(coinType,id,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method,"id":id}
        sign=signature(params)
        params['sign']=sign
        del params['secret_key']

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    '''
    限价卖出
    @param coinType
    @param price
    @param amount
    @param tradePassword
    @param tradeid
    '''
    def sell(coinType,price,amount,tradePassword,tradeid,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"price":price,"coin_type":coinType,"amount":amount,"method":method}
        sign=signature(params)
        params['sign']=sign
        del params['secret_key']
        if tradePassword:
            params['trade_password']=tradePassword
        if tradeid:
            params['trade_id']=tradeid

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    '''
    市价卖出
    @param coinType
    @param amount
    @param tradePassword
    @param tradeid
    '''
    def sellMarket(coinType,amount,tradePassword,tradeid,method):
        timestamp = long(time.time())
        params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"amount":amount,"method":method}
        sign=signature(params)
        params['sign']=sign
        if tradePassword:
            params['trade_password']=tradePassword
        if tradeid:
            params['trade_id']=tradeid

        del params['secret_key']

        payload = urllib.urlencode(params)
        r = requests.post(HUOBI_SERVICE_API, params=payload)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None


