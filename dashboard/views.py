from django.shortcuts import render

# icon sdk
from . import dashboardrpc
from iconsdk.exception import JSONRPCException

from dashboard.cron import daily_dashboard_cron

from .models import DailyTransactions, WalletCount, RewardRate

import requests


def init_mode(request):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = True
    if 'navbar' not in request.session:
        request.session['navbar'] = True
    if 'fromAddress' not in request.session:
        request.session['fromAddress'] = 'none'

    context = {
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'fromAddress': request.session['fromAddress'],
        'section': 'DASHBOARD',
    }
    return context


def top20wallets():
    url = 'https://tracker.icon.foundation/v0/wallet/addrList'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()['data']
    return rjson


def main_info():
    url = 'https://tracker.icon.foundation/v3/main/mainInfo'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()['tmainInfo']
    return rjson


def tx24h():
    url = 'https://tracker.icon.foundation/v3/main/txCountIn24h'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    rjson = r.json()['data']
    return rjson


def rrep(delrate):
    r_min = 0.02
    r_max = 0.12
    r_point = 0.7
    rrep_result = ((r_max - r_min) / (r_point ** 2)) * ((delrate / 100) - r_point) ** 2 + r_min
    rrep3rate = round(rrep_result * 3 * 100, 2)
    return rrep3rate


def index(request, template='dashboard/dashboard.html', extra_context=None):
    context = init_mode(request)

    #daily_dashboard_cron()

    #####################################################################################
    # Top wallets
    #####################################################################################
    t20 = top20wallets()
    ret20 = []
    count = 0
    tokens_total = 0
    percent_total = 0
    for wallet in t20:
        tokens_total += float(wallet['balance'])
        percent_total += float(wallet['percentage'])
        if(count == 0):
            ret20.append({'name': wallet['address'], 'y': wallet['percentage'], 'tokens': wallet['balance'], 'sliced': 'true', 'selected': 'true'})
        else:
            ret20.append({'name': wallet['address'], 'tokens': wallet['balance'], 'y': wallet['percentage']})
        count += 1

    #####################################################################################
    # Main Info
    #####################################################################################
    maininfo = main_info()
    total_supply = maininfo['icxSupply']
    marketcap = maininfo['marketCap']
    circulating_supply = maininfo['icxCirculationy']
    public_treasury = maininfo['publicTreasury']

    remain_token = float(total_supply) - tokens_total
    remain_percent = 100 - percent_total
    ret20.append({'name': 'REMAINING ACCOUNTS', 'tokens': remain_token, 'y': remain_percent})

    #####################################################################################
    # Daily transactions
    #####################################################################################
    daily_txs = DailyTransactions.objects.all().order_by('targetDate')

    targetDates = []
    txCounts = []

    for entry in daily_txs:
        md = entry.targetDate.split("-")[1].lstrip("0") + '/' + entry.targetDate.split("-")[2].lstrip("0")
        targetDates.append(md)
        txCounts.append(entry.txCount)

    transactions_24h = tx24h()
    transactions_all = maininfo['transactionCount']

    #####################################################################################
    # Total Vote / Stake
    #####################################################################################
    params = {}
    try:
        preps = dashboardrpc.DashboardRPCCalls().json_rpc_call("getPReps", params)
    except JSONRPCException as e:
        print(str(e.message))

    total_voted = int(preps['totalDelegated'], 16)/10**18
    total_stake = int(preps['totalStake'], 16)/10**18

    #####################################################################################
    # Wallet Count
    #####################################################################################
    #get_wallet_count()
    wallet_counts = WalletCount.objects.all().order_by('selectDate')

    selectDates = []
    totalCounts = []
    balanceCounts = []

    for entry in wallet_counts:
        md = entry.selectDate.split("-")[1].lstrip("0") + '/' + entry.selectDate.split("-")[2].lstrip("0")
        selectDates.append(md)
        totalCounts.append(entry.totalCount)
        balanceCounts.append(entry.balanceCount)

    #####################################################################################
    # Reward Rate
    #####################################################################################
    rewardrate = RewardRate.objects.all().order_by('create_day')

    total_supply_list = []
    annual_reward_list = []
    reward_rate_dates_list = []
    for entry in rewardrate:
        total_supply_list.append(entry.total_supply)
        annual_reward_list.append(rrep(entry.total_delegation/entry.total_supply*100))
        reward_rate_dates_list.append(str(entry.create_day).split("-")[1].lstrip("0")+"/"+str(entry.create_day).split("-")[2].lstrip("0"))

    annual_reward_list.pop(0)
    reward_rate_dates_list.pop(0)

    annual_inflation_list = []
    for i in range(len(total_supply_list)):
        if i >= 1:
            daily_rate = total_supply_list[i]/total_supply_list[i-1]-1
            annual_rate = round(((daily_rate+1)**365-1)*100, 2)
            annual_inflation_list.append(annual_rate)

    #print(delegation_rate_list)
    #print(inflation_rate_list)

    context.update({
        'ret20': ret20,
        'targetDates': targetDates,
        'txCounts': txCounts,
        'transactions_24h': transactions_24h,
        'transactions_all': transactions_all,

        'marketcap': marketcap,
        'circulating_supply': circulating_supply,
        'total_supply': total_supply,
        'public_treasury': public_treasury,
        'total_voted': total_voted,
        'total_stake': total_stake,

        'selectDates': selectDates,
        'totalCounts': totalCounts,
        'balanceCounts': balanceCounts,

        'annual_reward_list': annual_reward_list,
        'annual_inflation_list': annual_inflation_list,
        'reward_rate_dates_list': reward_rate_dates_list,
    })
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def preplist(request, type):
    context = init_mode(request)
    context.update({
        'section': 'P-REP LISTING'
    })
    return render(request, 'dashboard/preplist.html', context)
