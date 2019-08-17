from django.shortcuts import render

# icon sdk test
from . import jsonrpc

# coinmarketcap test
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def index(request):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = False
    if 'navbar' not in request.session:
        request.session['navbar'] = True
    if 'fromAddress' not in request.session:
        request.session['fromAddress'] = 'none'

    # ICON SDK test
    latest_block = jsonrpc.JsonRPCCalls().getLatestBlock()
    print(latest_block)


    # COINMARKETCAP (conversion for multiple currencies requires paid account, pay and refactor this later)
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'id': '2722', #AC3=2722, ICX=2099, USD=2781
        'convert': 'ICX'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'abd96001-925b-40d1-8160-9e02a66e7f5a',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        ac3data = data["data"]["2722"]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    context = {
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'fromAddress': request.session['fromAddress'],
        'section': 'DASHBOARD',
        'ac3data': ac3data,
    }

    return render(request, 'dashboard/dashboard.html', context)


def preplist(request, type):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = False
    if 'navbar' not in request.session:
        request.session['navbar'] = True

    context = {
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'section': 'P-REP LISTING',
    }

    return render(request, 'dashboard/preplist.html', context)

