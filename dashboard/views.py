from django.shortcuts import render

# icon sdk
from . import dashboardrpc
from iconsdk.exception import JSONRPCException

from .models import DailyTransactions, WalletCount, RewardRate, Top20Wallets, MainInfo, TopDapps, SocialInfo

import json

from dashboard.cron import get_top_dapps


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


def rrep(delrate):
    r_min = 0.02
    r_max = 0.12
    r_point = 0.7
    rrep_result = ((r_max - r_min) / (r_point ** 2)) * ((delrate / 100) - r_point) ** 2 + r_min
    rrep3rate = round(rrep_result * 3 * 100, 2)
    return rrep3rate


def index(request, template='dashboard/dashboard.html', extra_context=None):
    context = init_mode(request)
    #get_top_dapps()
    #dashboard_cron_1h()
    #####################################################################################
    # Top wallets
    #####################################################################################
    t20 = Top20Wallets.objects.all()[0].t20json
    t20 = t20.replace("\'", "\"")
    t20 = json.loads(t20)
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

    maininfo = MainInfo.objects.all()[0].maininfo_json
    maininfo = maininfo.replace("\'", "\"")
    maininfo = json.loads(maininfo)

    total_supply = maininfo['icxSupply']
    marketcap = maininfo['marketCap']
    circulating_supply = maininfo['icxCirculationy']
    public_treasury = maininfo['publicTreasury']

    remain_token = float(total_supply) - tokens_total
    remain_percent = 100 - percent_total
    ret20.append({'name': 'OTHER ACCOUNTS', 'tokens': remain_token, 'y': remain_percent})

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

    transactions_24h = daily_txs.last().tx24h
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
    total_staked = int(preps['totalStake'], 16)/10**18

    #####################################################################################
    # Wallet Count
    #####################################################################################
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
    annual_real_yield_list = []
    reward_rate_dates_list = []
    for entry in rewardrate:
        total_supply_list.append(entry.total_supply)
        annual_reward = rrep(entry.total_delegation/entry.total_supply*100)
        annual_reward_list.append(annual_reward)
        real_yield = annual_reward - 8.75
        annual_real_yield_list.append(round(real_yield, 2))
        reward_rate_dates_list.append(str(entry.create_day).split("-")[1].lstrip("0")+"/"+str(entry.create_day).split("-")[2].lstrip("0"))

    annual_reward_list.pop(0)
    reward_rate_dates_list.pop(0)
    annual_real_yield_list.pop(0)

    annual_inflation_list = []
    for i in range(len(total_supply_list)):
        if i >= 1:
            daily_rate = total_supply_list[i]/total_supply_list[i-1]-1
            #annual_rate = round(((daily_rate+1)**365-1)*100, 2)
            annual_rate = round(((total_supply_list[i] - total_supply_list[i-1]) * 365 / total_supply_list[i])*100, 2)
            annual_inflation_list.append(annual_rate)

    #####################################################################################
    # Governance
    #####################################################################################
    total_supply = float(total_supply)
    total_staked_percent = round(total_staked / total_supply * 100, 2)
    total_voted_percent = round(total_voted / total_supply * 100, 2)
    circulate_staked_percent = round(total_staked / float(circulating_supply) * 100, 2)
    total_staked = int(total_staked)
    total_voted = int(total_voted)

    #####################################################################################
    # Top dApps
    #####################################################################################
    topdapps = TopDapps.objects.all().order_by('create_day')

    dapps_create_day_list = []

    daolette_txLastDay = []
    daolette_volumeLastDayInUSD = []
    daolette_dauLastDay = []

    daodice_txLastDay = []
    daodice_volumeLastDayInUSD = []
    daodice_dauLastDay = []

    daobj_txLastDay = []
    daobj_volumeLastDayInUSD = []
    daobj_dauLastDay = []

    stayge_txLastDay = []
    stayge_volumeLastDayInUSD = []
    stayge_dauLastDay = []

    somesing_txLastDay = []
    somesing_volumeLastDayInUSD = []
    somesing_dauLastDay = []

    for topdapp in topdapps:
        cd = str(topdapp.create_day).split("-")[1].lstrip("0") + '/' + str(topdapp.create_day).split("-")[2].lstrip("0")
        dapps_create_day_list.append(cd)

        dapp_json = topdapp.topdapps_json
        dapp_json = json.loads(dapp_json)['data']
        icx_price = topdapp.icx_price

        for dapp in dapp_json:
            if contract_name(dapp['url']) == 'ICONBet - DAOdice':
                daodice_txLastDay.append(dapp['txLastDay'])
                daodice_volumeLastDayInUSD.append(dapp['volumeLastDayInUSD']*icx_price)
                daodice_dauLastDay.append(dapp['dauLastDay'])

            if contract_name(dapp['url']) == 'ICONBet - DAOlette':
                daolette_txLastDay.append(dapp['txLastDay'])
                daolette_volumeLastDayInUSD.append(dapp['volumeLastDayInUSD']*icx_price)
                daolette_dauLastDay.append(dapp['dauLastDay'])

            if contract_name(dapp['url']) == 'ICONBet - DAOblackjack':
                daobj_txLastDay.append(dapp['txLastDay'])
                daobj_volumeLastDayInUSD.append(dapp['volumeLastDayInUSD']*icx_price)
                daobj_dauLastDay.append(dapp['dauLastDay'])

            if contract_name(dapp['url']) == 'Stayge':
                stayge_txLastDay.append(dapp['txLastDay'])
                stayge_volumeLastDayInUSD.append(dapp['volumeLastDayInUSD']*icx_price)
                stayge_dauLastDay.append(dapp['dauLastDay'])

            if contract_name(dapp['url']) == 'Somesing':
                somesing_txLastDay.append(dapp['txLastDay'])
                somesing_volumeLastDayInUSD.append(dapp['volumeLastDayInUSD']*icx_price)
                somesing_dauLastDay.append(dapp['dauLastDay'])

    #####################################################################################
    # Social Info
    #####################################################################################
    socialinfo = SocialInfo.objects.all().order_by('-create_day').first()
    average_sentiment_calc_24h = round(socialinfo.average_sentiment_calc_24h / 5 * 100)
    average_sentiment_calc_24h_percent = socialinfo.average_sentiment_calc_24h_percent - 100
    social_score_calc_24h = socialinfo.social_score_calc_24h
    social_score_calc_24h_percent = socialinfo.social_score_calc_24h_percent - 100
    social_volume_calc_24h = socialinfo.social_volume_calc_24h
    social_volume_calc_24h_percent = socialinfo.social_volume_calc_24h_percent - 100

    context.update({
        'ret20': ret20,
        'targetDates': targetDates,
        'txCounts': txCounts,
        'transactions_24h': transactions_24h,
        'transactions_all': transactions_all,

        'marketcap': marketcap,
        'circulating_supply': circulating_supply,
        'total_supply': total_supply,
        'public_treasury': int(float(public_treasury)),
        'total_voted': int(total_voted),
        'total_staked': int(total_staked),
        'total_staked_percent': total_staked_percent,
        'total_voted_percent': total_voted_percent,
        'circulate_staked_percent': circulate_staked_percent,

        'selectDates': selectDates,
        'totalCounts': totalCounts,
        'balanceCounts': balanceCounts,

        'annual_reward_list': annual_reward_list,
        'annual_real_yield_list': annual_real_yield_list,
        'annual_inflation_list': annual_inflation_list,
        'reward_rate_dates_list': reward_rate_dates_list,

        'dapps_create_day_list': dapps_create_day_list,
        'daodice_txLastDay': daodice_txLastDay,
        'daodice_volumeLastDayInUSD': daodice_volumeLastDayInUSD,
        'daodice_dauLastDay': daodice_dauLastDay,

        'daolette_txLastDay': daolette_txLastDay,
        'daolette_volumeLastDayInUSD': daolette_volumeLastDayInUSD,
        'daolette_dauLastDay': daolette_dauLastDay,

        'daobj_txLastDay': daolette_txLastDay,
        'daobj_volumeLastDayInUSD': daolette_volumeLastDayInUSD,
        'daobj_dauLastDay': daolette_dauLastDay,

        'stayge_txLastDay': stayge_txLastDay,
        'stayge_volumeLastDayInUSD': stayge_volumeLastDayInUSD,
        'stayge_dauLastDay': stayge_dauLastDay,

        'somesing_txLastDay': somesing_txLastDay,
        'somesing_volumeLastDayInUSD': somesing_volumeLastDayInUSD,
        'somesing_dauLastDay': somesing_dauLastDay,

        'average_sentiment_calc_24h': average_sentiment_calc_24h,
        'average_sentiment_calc_24h_percent': average_sentiment_calc_24h_percent,
        'social_score_calc_24h': social_score_calc_24h,
        'social_score_calc_24h_percent': social_score_calc_24h_percent,
        'social_volume_calc_24h': social_volume_calc_24h,
        'social_volume_calc_24h_percent': social_volume_calc_24h_percent,
    })

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def contract_name(address):
    contract_mapping = {
        "cxb0b6f777fba13d62961ad8ce11be7ef6c4b2bcc6": "ICONBet - DAOdice",
        "cx1b97c1abfd001d5cd0b5a3f93f22cccfea77e34e": "ICONBet - DAOlette",
        "cxd47f7d943ad76a0403210501dab03d4daf1f6864": "ICONBet - DAOblackjack",
        "cx502c47463314f01e84b1b203c315180501eb2481": "Stayge",
        "cx429731644462ebcfd22185df38727273f16f9b87": "Somesing"
    }
    if contract_mapping.get(address) != None:
        return contract_mapping[address]
    else:
        return address
