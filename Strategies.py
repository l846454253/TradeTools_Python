from System import *
from Util import *
from huobi import RequestClient
from huobi.model import Account
import json
'''
 普通定投（指定区间（可选）， 指定周期（可选）， 指定定投总资金（可选）， 指定每次定投的资金量（必选））
 支持多个币种定投， 通过配置文件进行配置
'''
def GetSpotAccountBalances(coin):
    request_client = RequestClient(api_key=ACCESS_KEY, secret_key=SECRET_KEY)
    account_balance_list = request_client.get_account_balance()
    if account_balance_list and len(account_balance_list):
        for account in account_balance_list:
            if account.account_type == "spot":
                if account.balances and len(account.balances):
                    for balance in account.balances:
                        if balance.currency == coin and balance.balance_type == "trade":
                            return balance.balance

'''
回调方法 交易前准备工作
如果没交易成功，如何处理，轮询还是如何
'''
def AutomaticInvestment(conf):
    dict=json.loads(conf)

    # 循环遍历每个币种
    for conf in dict["conf"]:
        coin=conf["coin"]
        limit=conf["limit"]
        amount=conf["amount"]
        total_amount = conf["total_amount"]

        # 获取指数价格 是否在定投区间
        '''
        Timestamp : 1599408134086
        Open : 10269.24     24h前的价格
        Close : 10156.84    当前价格
        Amount : 74141.55194223553  24h成交量
        High : 10300.83     24h最高价
        Low : 9834.77   24h最低价
        Count : 830654
        Volume : 749859976.568394
        '''
        request_client = RequestClient()
        trade_statistics = request_client.get_24h_trade_statistics(coin)
        cur_price=trade_statistics.close
        if cur_price > limit:
            print(f"{coin} cur_price:{cur_price}")
            print(f"{coin} limit:{limit}")
            print(f"{coin} price is too high! so giveup trade!")
            return None

        #查询币币账户余额 目前只支持USDT对
        # 原则：余额a 每次定投资金b
        # a >= b 交易量为b
        # a < b 交易量为a
        # a = 0 返回
        Balance=GetSpotAccountBalances("usdt")
        if Balance == 0:
            return None
        if Balance >= amount:
            real=amount
        elif Balance < amount:
            real=Balance

        print(real)






#获取定投币的余额 是否超过了额度

#交易时优先用USDT交易， 如果没有U对， 或没有足够的USDT， 用BTC>HT>ETH的顺序进行交易

'''
定时器回调（每晚00:00触发）或推送最新价格时触发回调
'''
data='''
{
	"conf": [{
		"coin": "btcusdt",
		"limit": 10300,
		"amount": 10,
		"total_amount": 100
	}, {
		"coin": "ethusdt",
		"limit": 400,
		"amount": 10,
		"total_amount": 100
	}]
}
'''

ScheduleTimer(data, AutomaticInvestment, "seconds")
