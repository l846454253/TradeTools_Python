from huobi import RequestClient
from huobi.constant.test import *
from huobi.base.printobject import *
from huobi.model import Account
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
account_balance_list = request_client.get_accounts()
if account_balance_list and len(account_balance_list):
    for account in account_balance_list:
        print("======= ID", account.id, "=======")
        print("Account Status", account.account_state)
        print("Account Type", account.account_type)
        print("Subtype", account.subtype)
        print()


