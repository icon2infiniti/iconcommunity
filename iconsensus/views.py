from django.shortcuts import render
from .models import CorePrep

from django.contrib.staticfiles.templatetags.staticfiles import static


def init_mode(request):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = True
    if 'navbar' not in request.session:
        request.session['navbar'] = True
    if 'fromAddress' not in request.session:
        request.session['fromAddress'] = 'none'

    context = {
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'fromAddress': request.session['fromAddress'],
        'section': 'ICONSENSUS',
    }
    return context


def about(request):
    context = init_mode(request)
    context.update({
        'subsection': 'ABOUT',
    })
    return render(request, 'iconsensus/about.html', context)


# Get market data
def get_map_marker(prep):
    position = prep.server_location_latlong.replace('(', '').replace(')', '').strip().split(',')
    url = '/iconsensus/candidate_detail/'+str(prep.id)+'/'
    if position and len(position) > 1:
        data = {
            'icon': static('iconsensus/img/'+prep.logo),
            'position': {
                'lat': position[0],
                'lng': position[1]
            },
            'url': url
        }
    return data


def candidates(request):
    context = init_mode(request)
    preps = CorePrep.objects.using('prepsqlite3').filter(display=True).order_by('-id')
    total = CorePrep.objects.using('prepsqlite3').filter(display=True).count

    # Prepare Database Prep Map Locations
    locations = []
    for prep in preps:
        try:
            location = get_map_marker(prep)
            if location:
                locations.append(location)
        except Exception as e:
            pass

    context.update({
        'subsection': 'CANDIDATES',
        'preps': preps,
        'prep_locations': locations,
        'total': total,
    })
    return render(request, 'iconsensus/candidates.html', context)


def candidate_detail(request, pk):
    context = init_mode(request)
    prep = CorePrep.objects.using('prepsqlite3').get(pk=pk)

    context.update({
        'subsection': 'CANDIDATES',
        'prep': prep,
    })
    return render(request, 'iconsensus/candidate_detail.html', context)
