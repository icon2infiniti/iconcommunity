from django.http import HttpResponse
import json


def toggle_nightmode(request):
    request.session['nightmode'] = not request.session['nightmode']
    return HttpResponse(json.dumps({'nightmode': request.session['nightmode']}), content_type="application/json")


def toggle_navbar(request):
    request.session['navbar'] = not request.session['navbar']
    return HttpResponse(json.dumps({'navbar': request.session['navbar']}), content_type="application/json")


def set_wallet(request, fromAddress):
    request.session['fromAddress'] = fromAddress
    return HttpResponse(json.dumps({'fromAddress': request.session['fromAddress']}), content_type="application/json")
