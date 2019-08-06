from django.shortcuts import render

# icon sdk test
#from iconsdk.icon_service import IconService
#from iconsdk.providers.http_provider import HTTPProvider

# coinmarketcap test
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def index(request):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = False
    if 'navbar' not in request.session:
        request.session['navbar'] = True

    # ICON SDK test
    #icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io/api/v3"))
    #latestblock = icon_service.get_block("latest")

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

