#coding=utf-8

from Util import *
from huobi import HuobiService

HuobiSpot=HuobiSpot(ACCESS_KEY, SECRET_KEY, HUOBI_SERVICE_API)

if __name__ == "__main__":
    print("查询账户信息")
    print(HuobiSpot.getAccountInfo())


