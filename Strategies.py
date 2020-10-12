from System import *
from Util import *
# from huobi import RequestClient
# from huobi.model import Account
import json
import logging

'''
 普通定投（指定区间（可选）， 指定周期（可选）， 指定定投总资金（可选）， 指定每次定投的资金量（必选））
 支持多个币种定投， 通过配置文件进行配置

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


回调方法 交易前准备工作
如果没交易成功，如何处理，轮询还是如何

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
        
        Timestamp : 1599408134086
        Open : 10269.24     24h前的价格
        Close : 10156.84    当前价格
        Amount : 74141.55194223553  24h成交量
        High : 10300.83     24h最高价
        Low : 9834.77   24h最低价
        Count : 830654
        Volume : 749859976.568394
        
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








定时器回调（每晚00:00触发）或推送最新价格时触发回调




定投币种：
开始定投时间：
预计结束时间：
预计定投次数：
定投最高价格：
定投周期：
每次定投金额：
总投资金额：

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
'''


# 作用：定时完成一次交易
# 生命周期：完成交易后终止
def TimerForTrade(conf):
    print('hello')
    pass
    # 开启交易
    # 打印交易信息
    # 交易
    # 出错处理


'''
type1
总量 / 每次 = 次数
次数 * 间隔 = 总时间

给出的情况：（总时间无法给出）
总量，每次，间隔
次数，总量，间隔
次数，每次，间隔

种参数同时出现时，处理如下：
优先度：总量 > 每次 > 间隔 > 次数
总量，每次，间隔
次数，总量，间隔
次数，每次，间隔
'''
# 启动定投线程，线程里面开定时器，定时器里面继续扫描配置，实时操作，每次操作必须同步参数计数

# 作用：启动定时器
# 生命周期：直到定投任务完成
def ThreadWork(*args):
    TimerRunFlag = False
    TimerIntervalRecord = 0;

    while True:
        JsonContext = JsonFileLoad(args[0])
        # 循环遍历每个币种
        for conf in JsonContext["conf"]:
            coin = conf["coin"]
            base = conf["base"]
            status = conf["status"]
            coinbase = coin + base
            isThreadOn = False

            # 打开则判断该币种的定投线程是否还在工作
            if threading.current_thread().getName() == coinbase:
                isThreadOn = True
                break

        # 判断配置文件定投开关是否打开
        if status == TradeStatus.ON:
            pass
        elif status == TradeStatus.OFF:   
            isThreadOn = False
        elif status == TradeStatus.SUSPEND:   #暂停，线程不结束
            schedule.clear(threading.current_thread().getName())
            TimerRunFlag = False
            continue
        else:
            isThreadOn = False

        if isThreadOn == False:
            schedule.clear(threading.current_thread().getName())
            return 
            
        #解析json
        amount = conf["amount"]
        total_amount = conf["total_amount"]
        times = conf["times"]
        for timer in conf["timer"]:
            timer_type = timer["type"]
            Time = timer["time"]
            if timer_type == 1:   #定投间隔
                str = "%2d:%2d:%2d:%2d:%2d:%2d" % (
                Time["mon"], Time["week"], Time["day"], Time["hour"], Time["min"], Time["sec"])
                time_interval = Time2Sec(str, timer_type)
                if time_interval:
                    if TimerIntervalRecord != time_interval or TimerRunFlag == False:
                        schedule.clear(coinbase)    #取消上次任务
                        ScheduleTimer(args[0], TimerForTrade, "seconds", time_interval, Tag=coinbase)
                        TimerRunFlag = True #表示任务已添加，不能重复添加任务
                        TimerIntervalRecord = time_interval
                else:
                    schedule.clear(coinbase)    #取消上次任务
                    
            elif timer_type == 2: #指定周期内具体某个时间定投
                if Time["mon"]:
                   pass
            elif timer_type == 3: #指定时间内定投完毕
                pass
                
        time.sleep(1)

    '''
    if type == 0:
        if total_amount and amount and interval:

        elif total_amount and times and interval:

        elif amount and times and interval:

        else:
        #这里只启动定时器，是否符合定投条件不在这里判断

        #解析定投信息，启动定时器
            #判断开关是否打开
                #非打开状态，退出
                #打开状态，继续
            #判断条件
                #是否达成定投目标
                #达成则终止线程   
        #启动定时器
    '''


# 作用：负责开启任务线程
# 生命周期：直到程序被杀死
def ThreadConfigureScanner(*args):
    while True:
        JsonContext = JsonFileLoad(args[0])
        # 循环遍历每个币种
        for conf in JsonContext["conf"]:
            coin = conf["coin"]
            base = conf["base"]
            status = conf["status"]
            coinbase = str(coin + base)
            isThreadOn = False

            # 判断配置文件定投开关是否打开
            if status == TradeStatus.ON:
                # 打开则判断该币种的定投线程是否还在工作
                for i in threading.enumerate():
                    if i.name == coinbase:
                        isThreadOn = True

                # 未工作，准备启动
                if isThreadOn == False:
                    print("create")
                    ThreadCreate(ThreadWork, (args[0],), coinbase)

        # 启动定时器任务
        schedule.run_pending()

        time.sleep(1)


def AutomaticInvestmentTradeStart(conf_path):
    # 启动配置文件扫描线程
    ThreadCreate(ThreadConfigureScanner, (conf_path,))


AutomaticInvestmentTradeStart(AUTO_INVEST_CONF_FILE)
