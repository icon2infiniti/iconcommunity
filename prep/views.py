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


def get_prep(address):
    params = {
        'address': address
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls(
            "cx0000000000000000000000000000000000000000").json_rpc_call("getPRep", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def get_preps():
    params = {
        'startRanking': "0x1",
        'endRanking': "0x8",
        'blockHeight': "0x1234"
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls(
            "cx0000000000000000000000000000000000000000").json_rpc_call("getPReps", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def get_proposal(proposal_id):
    params = {
        'id': proposal_id
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls(
            "cx0000000000000000000000000000000000000001").json_rpc_call("getProposal", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def get_block(blockHeight):
    block = preprpc.PrepRPCCalls(
        "cx0000000000000000000000000000000000000001").get_block(int(blockHeight, 16))
    return block


"""
    params = {
        'value': blockHeight
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls(
            "cx0000000000000000000000000000000000000000").json_rpc_call("getBlock", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response
"""


def get_transaction(txHash):
    params = {
        'tx_hash': txHash
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls(
            "cx0000000000000000000000000000000000000000").json_rpc_call("getTransaction", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def management(request, template='prep/management.html'):
    context = init_mode(request)

    #latest_block = preprpc.PrepRPCCalls("cx0000000000000000000000000000000000000000").json_rpc_call("getLastBlock", params)
    #latest_block = preprpc.PrepRPCCalls("cx8e50eb4188681401aee7bd29178ed451f558697c").json_rpc_call("showGameRoomList", params)

    getPRep = get_prep(request.session['fromAddress'])
    context.update({
        'getPRep': getPRep
    })
    context["USE_NET_NAME"] = preprpc.PrepRPCCalls.USE_NET_NAME

    # context.update({
    #    'latest_block': latest_block,
    # })

    return render(request, template, context)


def governance(request, template='prep/governance.html'):
    context = init_mode(request)
    PReps = get_preps()
    if PReps != None:
        context["dataList"] = PReps['preps']

    getPRep = get_prep(request.session['fromAddress'])
    if getPRep != None:
        context.update({
            'getPRep': getPRep
        })
    context["USE_NET_NAME"] = preprpc.PrepRPCCalls.USE_NET_NAME

    return render(request, template, context)


def proposal(request, template='prep/proposal.html'):
    context = init_mode(request)

    getPRep = None
    try:
        getPRep = get_prep(request.session['fromAddress'])
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        context.update({
            'getPRep': getPRep
        })
        context["USE_NET_NAME"] = preprpc.PrepRPCCalls.USE_NET_NAME

        return render(request, template, context)


def newproposal(request, template='prep/newproposal.html'):
    context = init_mode(request)

    getPRep = get_prep(request.session['fromAddress'])
    context.update({
        'getPRep': getPRep
    })
    context["USE_NET_NAME"] = preprpc.PrepRPCCalls.USE_NET_NAME

    return render(request, template, context)


def proposaldetail(request, proposal_id):
    context = init_mode(request)
    aProposal = get_proposal(proposal_id)
    if aProposal != None:
        context['aProposal'] = aProposal

        startBlock = get_block(aProposal['startBlockHeight'])
        if startBlock != None:
            context['start'] = startBlock['time_stamp']

        endBlock = get_block(aProposal['endBlockHeight'])
        if endBlock != None:
            context['end'] = endBlock['time_stamp']
        else:
            context['end'] = aProposal['endBlockHeight']

        aPRep = get_prep(aProposal['proposer'])
        if aPRep != None:
            context['aPRep'] = aPRep

    getPRep = get_prep(request.session['fromAddress'])
    if getPRep != None:
        context.update({
            'getPRep': getPRep
        })

    context["USE_NET_NAME"] = preprpc.PrepRPCCalls.USE_NET_NAME

    return render(request, 'prep/proposaldetail.html', context)
