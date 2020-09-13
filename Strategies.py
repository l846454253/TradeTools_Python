from System import *
from Util import *
from huobi import RequestClient
from huobi.model import Account
import json
import logging

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
        base=conf["base"]
        limit=conf["limit"] #可选
        amount=conf["amount"]   #必选
        total_amount = conf["total_amount"] #可选

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
        request_client = RequestClient(api_key=ACCESS_KEY, secret_key=SECRET_KEY)
        trade_statistics = request_client.get_24h_trade_statistics(coin+base)
        cur_price=trade_statistics.close
        if limit and cur_price > limit:
            print(f"{coin} 当前价格:{cur_price}")
            print(f"{coin} 限制价格:{limit}")
            print(f"{coin} 价格过高，放弃本次交易!")
            continue

        #获取定投币的余额 是否超过了额度 需要查询历史订单 当前余额会因为价格涨跌而无法判断定投消耗的真实资金
        Balance=float(GetSpotAccountBalances(coin))
        BalanceWorth=Balance*cur_price          #只支持U对，如果使用非U对，要改动这里
        if total_amount and BalanceWorth > total_amount:
            print(f"{coin} 余额价值:{BalanceWorth}")
            print(f"{coin} 总定投金额:{total_amount}")
            print(f"{coin} 定投计划已达标，放弃本次交易!")
            continue

        #查询币币账户余额 目前只支持USDT对
        # 原则：余额a 每次定投资金b
        # a >= b 交易量为b
        # a < b 交易量为a
        # a = 0 返回
        Balance=float(GetSpotAccountBalances(base))
        if Balance == 0:    #后续可优化成计算出最小交易金额的方式过滤
            continue
        if Balance >= amount:
            real_amount=float(amount)
        elif Balance < amount:
            real_amount=float(Balance)

        #交易时优先用USDT交易， 如果没有U对， 或没有足够的USDT， 用BTC>HT>ETH的顺序进行交易
        #暂时只支持用USDT    
        request = request_client.create_order(coin+base, AccountType.SPOT, OrderType.BUY_MARKET, real_amount, cur_price)
        request.print_object()
        
        #查看交易状态







'''
定时器回调（每晚00:00触发）或推送最新价格时触发回调
'''
data='''
{
	"conf": [{
		"coin": "btc",
		"base": "usdt"
		"limit": 10300,
		"amount": 10,
		"total_amount": 100
		"time"
	}, {
		"coin": "eth",
		"base": "usdt"
		"limit": 400,
		"amount": 10,
		"total_amount": 100
	}]
}
'''
定投币种：
开始定投时间：
预计结束时间：
预计定投次数：
定投最高价格：
定投周期：
每次定投金额：
总投资金额：
'''
def AutomaticInvestmentPrintTradeStart(conf):
    logger=FileLoggingInit(AUTO_INVEST_LOG_FILE)
    logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  
    # 循环遍历每个币种
    dict=json.loads(conf)
    for conf in dict["conf"]:
        coin=conf["coin"]
        base=conf["base"]
        limit=conf["limit"] #可选
        amount=conf["amount"]   #必选
        total_amount = conf["total_amount"] #可选

        logger.info("定投币种：{}", format(coin))
        # 获得当前时间时间戳
        start=int(time.time())
        logger.info("开始定投时间：{}", format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))))
        end=
        logger.info("预计结束时间：{}", format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

        
    
ScheduleTimer(data, AutomaticInvestment, "seconds")
