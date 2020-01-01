from .models import DailyTransactions
import requests


def get_daily_transactions():
    print("Daily Transactions!")

    url = 'https://tracker.icon.foundation/v0/main/mainChart'
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
