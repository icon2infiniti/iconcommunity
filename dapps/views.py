from django.shortcuts import render
from .models import TXChallenge, OfficialDapps


def dapps(request, template='dapps/dapps.html', extra_context=None):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = True
    if 'navbar' not in request.session:
        request.session['navbar'] = True
    if 'fromAddress' not in request.session:
        request.session['fromAddress'] = 'none'

    tx_challenges = TXChallenge.objects.filter(display=True).order_by('-id')
    official_dapps = OfficialDapps.objects.filter(display=True).order_by('-id')

    context = {
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'fromAddress': request.session['fromAddress'],
        'section': 'DAPPS',
        'tx_challenges': tx_challenges,
        'official_dapps': official_dapps,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
