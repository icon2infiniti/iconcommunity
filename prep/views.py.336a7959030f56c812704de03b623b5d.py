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
        # 'address': request.session['fromAddress']
        # 'address': 'hxb2ed93806e9585a7a8b722f7031323925914de91'
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls().json_rpc_call("getPRep", params)
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
    response = preprpc.PrepRPCCalls().json_rpc_call("getPReps", params)
    return response


def get_proposal(proposal_id):
    params = {
        'id': proposal_id
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls().json_rpc_call("getProposal", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def get_block(blockHeight):
    params = {
        'value': blockHeight
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls().json_rpc_call("getBlock", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def get_transaction(txHash):
    params = {
        'tx_hash': txHash
    }
    response = None
    try:
        response = preprpc.PrepRPCCalls().json_rpc_call("getTransaction", params)
    except JSONRPCException as e:
        print(str(e.message))
    finally:
        return response


def management(request, template='prep/management.html'):
    context = init_mode(request)

    #latest_block = preprpc.PrepRPCCalls().json_rpc_call("getLastBlock", params)
    #latest_block = preprpc.PrepRPCCalls("cx8e50eb4188681401aee7bd29178ed451f558697c").json_rpc_call("showGameRoomList", params)

    getPRep = get_prep(request.session['fromAddress'])
    context.update({
        'getPRep': getPRep
    })

    # context.update({
    #    'latest_block': latest_block,
    # })

    return render(request, template, context)


def governance(request, template='prep/governance.html'):
    context = init_mode(request)
    PReps = get_preps()
    context["dataList"] = PReps['preps']

    getPRep = get_prep(request.session['fromAddress'])
    context.update({
        'getPRep': getPRep
    })

    return render(request, template, context)


def proposal(request, template='prep/proposal.html'):
    context = init_mode(request)

    getPRep = get_prep(request.session['fromAddress'])
    context.update({
        'getPRep': getPRep
    })

    return render(request, template, context)


def newproposal(request, template='prep/newproposal.html'):
    context = init_mode(request)

    getPRep = get_prep(request.session['fromAddress'])
    context.update({
        'getPRep': getPRep
    })

    return render(request, template, context)


def proposaldetail(request, proposal_id):
    context = init_mode(request)
    aProposal = get_proposal(proposal_id)
    context['aProposal'] = aProposal
    aPRep = get_prep(aProposal['proposer'])
    context['aPRep'] = aPRep
    startBlock = get_block(aProposal['startBlockHeight'])
    endBlock = get_block(aProposal['endBlockHeight'])
    context['start'] = startBlock['time_stamp']
    context['end'] = endBlock['time_stamp']

    getPRep = get_prep(request.session['fromAddress'])
    context.update({
        'getPRep': getPRep
    })

    return render(request, 'prep/proposaldetail.html', context)
