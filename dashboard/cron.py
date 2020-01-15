from .models import DailyTransactions, WalletCount, RewardRate, Top20Wallets, MainInfo
import requests

from . import dashboardrpc
from iconsdk.exception import JSONRPCException

import datetime


def tx24h():
    url = 'https://tracker.icon.foundation/v3/main/txCountIn24h'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()['data']
    return rjson


def get_daily_transactions():
    print("Daily Transactions: "+str(datetime.datetime.now()))

    url = 'https://tracker.icon.foundation/v3/main/mainChart'
    try:
        txs = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)

    tx_json = txs.json()
    transactions_24h = tx24h()

    for entry in tx_json['data']:
        DailyTransactions.objects.update_or_create(
            targetDate=entry['targetDate'].split("T")[0],
            defaults={'targetDate': entry['targetDate'].split("T")[0], 'txCount': entry['txCount'], 'tx24h': transactions_24h}
        )


def get_wallet_count():
    print("Wallet Count: "+str(datetime.datetime.now()))

    url = 'https://tracker.icon.foundation/v3/address/count'
    try:
        wc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)

    wc = wc.json()['data']

    WalletCount.objects.update_or_create(
        selectDate=wc['selectDate'].split("T")[0],
        defaults={'selectDate': wc['selectDate'].split("T")[0], 'balanceCount': wc['balanceCount'], 'totalCount': wc['totalCount']}
    )


def get_reward_rate():
    print("Reward Rate: "+str(datetime.datetime.now()))

    params = {}
    try:
        preps = dashboardrpc.DashboardRPCCalls().json_rpc_call("getPReps", params)
    except JSONRPCException as e:
        print(str(e.message))
    total_delegation = int(preps['totalDelegated'], 16)/10**18

    url = 'https://tracker.icon.foundation/v3/main/mainInfo'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)

    rjson = r.json()['tmainInfo']
    total_supply = float(rjson['icxSupply'])
    circ_supply = float(rjson['icxCirculationy'])
    transactionCount = int(rjson['transactionCount'])
    publicTreasury = float(rjson['publicTreasury'])

    RewardRate.objects.update_or_create(
        create_day=datetime.date.today(),
        defaults={
            'total_delegation': total_delegation,
            'total_supply': total_supply,
            'circ_supply': circ_supply,
            'transactionCount': transactionCount,
            'publicTreasury': publicTreasury,
            'create_day': datetime.date.today()
        }
    )


def get_top20_wallets():
    url = 'https://tracker.icon.foundation/v0/wallet/addrList'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()['data']

    Top20Wallets.objects.all().delete()
    t20wallets = Top20Wallets()
    t20wallets.t20json = rjson
    t20wallets.save()


def get_main_info():
    url = 'https://tracker.icon.foundation/v3/main/mainInfo'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()['tmainInfo']

    MainInfo.objects.all().delete()
    maininfo = MainInfo()
    maininfo.maininfo_json = rjson
    maininfo.save()


def dashboard_cron_6h():
    get_daily_transactions()
    get_wallet_count()
    get_reward_rate()
    get_top20_wallets()
    get_main_info()
