from django.shortcuts import render
from . import preprpc

def registration(request, template='prep/registration.html', extra_context=None):
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
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def management(request, template='prep/management.html', extra_context=None):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = False
    if 'navbar' not in request.session:
        request.session['navbar'] = True
    if 'fromAddress' not in request.session:
        request.session['fromAddress'] = 'none'

    latest_block = preprpc.PrepRPCCalls().getPReps()

    context = {
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'fromAddress': request.session['fromAddress'],
        'section': 'PREP',
        'latest_block': latest_block,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def governance(request, template='prep/governance.html', extra_context=None):
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
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def proposal(request, template='prep/proposal.html', extra_context=None):
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
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
