from .models import DailyTransactions, WalletCount, RewardRate
import requests

from . import dashboardrpc
from iconsdk.exception import JSONRPCException

import datetime


def get_daily_transactions():
    print("Daily Transactions!")

    url = 'https://tracker.icon.foundation/v3/main/mainChart'
    try:
        txs = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)

    tx_json = txs.json()

    for entry in tx_json['data']:
        DailyTransactions.objects.update_or_create(
            targetDate=entry['targetDate'].split("T")[0],
            defaults={'targetDate': entry['targetDate'].split("T")[0], 'txCount': entry['txCount']}
        )


def get_wallet_count():
    print("Wallet Count")

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
    print("Reward Rate")

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


def daily_dashboard_cron():
    get_daily_transactions()
    get_wallet_count()
    get_reward_rate()
