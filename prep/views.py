from django.shortcuts import render
from . import preprpc
from iconsdk.exception import JSONRPCException


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
        'section': 'PREP',
    }
    return context


def registration(request, template='prep/registration.html'):
    context = init_mode(request)
    return render(request, template, context)


def get_prep(request):
    params = {
        # 'address': request.session['fromAddress']
        'address': 'hxb2ed93806e9585a7a8b722f7031323925914de91'
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls().json_rpc_call("getPRep", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def get_preps(request):
    params = {
        'startRanking': "0x1",
        'endRanking': "0x8",
        'blockHeight': "0x1234"
    }
    response = preprpc.PrepRPCCalls().json_rpc_call("getPReps", params)
    return response


def management(request, template='prep/management.html'):
    context = init_mode(request)

    #latest_block = preprpc.PrepRPCCalls().json_rpc_call("getLastBlock", params)
    #latest_block = preprpc.PrepRPCCalls("cx8e50eb4188681401aee7bd29178ed451f558697c").json_rpc_call("showGameRoomList", params)

    getPRep = get_prep(request)
    context.update({
        'getPRep': getPRep
    })

    # context.update({
    #    'latest_block': latest_block,
    # })

    return render(request, template, context)


def governance(request, template='prep/governance.html'):
    context = init_mode(request)
    PReps = get_preps(request)
    PRep = get_prep(request)
    context["dataList"] = PReps['preps']
    context["irep"] = int(PRep['irep'], 0)
    context["irepUpdateBlockHeight"] = int(PRep['irepUpdateBlockHeight'], 0)
    print(context["irep"])
    print(context["irepUpdateBlockHeight"])
    return render(request, template, context)


def proposal(request, template='prep/proposal.html'):
    context = init_mode(request)
    return render(request, template, context)
