from .models import DailyTransactions, WalletCount, RewardRate, Top20Wallets, MainInfo, TopDapps, SocialInfo
import requests

from . import dashboardrpc
from iconsdk.exception import JSONRPCException

import datetime
import json


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
    print("Top 20 Wallets: " + str(datetime.datetime.now()))
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
    print("Main Info: " + str(datetime.datetime.now()))
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


def get_top_dapps():
    print("Top Dapps: " + str(datetime.datetime.now()))
    url = 'https://blockmove.eu/icon.json'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()

    price_r = requests.get('https://api.velic.io/api/v1/public/transaction?base_coin=USDT&match_coin=ICX')
    price_rjson = price_r.json()
    icx_price = price_rjson[0]['price']

    TopDapps.objects.update_or_create(
        create_day=datetime.date.today(),
        defaults={'topdapps_json': json.dumps(rjson), 'tx': r.json()['tx'], 'vol': r.json()['vol'], 'fee': r.json()['fee'], 'icx_price': icx_price, 'create_day': datetime.date.today()}
    )


def get_social_info():
    print("Social Info: " + str(datetime.datetime.now()))
    url = 'https://api.lunarcrush.com/v2?data=assets&key=07reb53h0wuwu9xn0aaw2ms&symbol=ICX'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()['data']

    create_day = datetime.datetime.fromtimestamp(rjson[0]['time']).strftime('%Y-%m-%d')

    average_sentiment_calc_24h = rjson[0]['average_sentiment_calc_24h'] #Average sentiment over the last 24 hours
    average_sentiment_calc_24h_percent = rjson[0]['average_sentiment_calc_24h_percent'] #Precent change in average sentiment 24 hours vs previous 24 hour period

    social_score_calc_24h = rjson[0]['social_score_calc_24h'] #Sum of social engagement over the last 24 hours
    social_score_calc_24h_percent = rjson[0]['social_score_calc_24h_percent'] #Precent change in social engagement over the last 24 hours vs previous 24 hour period

    social_volume_calc_24h = rjson[0]['social_volume_calc_24h'] #Number of social posts over the last 24 hours
    social_volume_calc_24h_percent = rjson[0]['social_volume_calc_24h_percent'] #Percent change in number if social posts over the last 24 hours vs previous 24 hour period

    SocialInfo.objects.update_or_create(
        create_day=create_day,
        defaults={
            'average_sentiment_calc_24h': average_sentiment_calc_24h,
            'average_sentiment_calc_24h_percent': average_sentiment_calc_24h_percent,
            'social_score_calc_24h': social_score_calc_24h,
            'social_score_calc_24h_percent': social_score_calc_24h_percent,
            'social_volume_calc_24h': social_volume_calc_24h,
            'social_volume_calc_24h_percent': social_volume_calc_24h_percent,
            'create_day': create_day
        }
    )


def dashboard_cron_6h():
    get_wallet_count()
    get_reward_rate()
    get_top20_wallets()
    get_main_info()


def dashboard_cron_1h():
    get_daily_transactions()
    get_top_dapps()
    get_social_info()
