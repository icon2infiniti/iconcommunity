from django.shortcuts import render

# icon sdk test
from . import dashboardrpc
from iconsdk.exception import JSONRPCException

# coinmarketcap test
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from el_pagination.decorators import page_template


def init_mode(request):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = False
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


@page_template('dashboard/prepranking_page.html')
def index(request, template='dashboard/dashboard.html', extra_context=None):
    context = init_mode(request)

    # GetPReps
    params = {}
    preps = {}
    try:
        preps = dashboardrpc.DashboardRPCCalls().json_rpc_call("getPReps", params)
    except JSONRPCException as e:
        print(str(e.message))

    PREP_GRADE = {0: 'Main P-Rep', 1: 'Sub P-Rep', 2: 'P-Rep'}

    i = 1
    for prep in preps['preps']:
        prep['index'] = i
        i += 1
        prep['grade'] = PREP_GRADE[int(prep['grade'], 16)]
        irep = int(int(prep['irep'], 16)/1000000000000000000)
        prep['irep'] = '{:,}'.format(irep)
        prep['stake'] = int(prep['stake'], 16)
        delegated = int(prep['delegated'], 16)/1000000000000000000
        prep['delegated'] = delegated = '{:,}'.format(delegated)
        prep['validatedBlocks'] = int(prep['validatedBlocks'], 16)
        prep['totalBlocks'] = int(prep['totalBlocks'], 16)

    prep_all = preps['preps']


    # CMC (conversion for multiple currencies requires paid account, pay and refactor this later)
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
        context.update({
            'ac3data': ac3data
        })
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    context.update({
        'prep_all': prep_all,
    })
    # END CMC
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def preplist(request, type):
    context = init_mode(request)
    context.update({
        'section': 'P-REP LISTING'
    })
    return render(request, 'dashboard/preplist.html', context)

