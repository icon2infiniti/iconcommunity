from .models import DailyTransactions, WalletCount
import requests


def daily_dashboard_cron():
    get_daily_transactions()
    get_wallet_count()


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