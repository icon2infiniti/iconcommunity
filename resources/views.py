from django.shortcuts import render
from .models import News, Press, VideoEvents, VideoInterviews, VideoIconsensus
from el_pagination.decorators import page_template


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
        'section': 'RESOURCES',
    }
    return context


@page_template('resources/video_iconsensus_page.html', key='video_iconsensus_page')
@page_template('resources/video_events_page.html', key='video_events_page')
@page_template('resources/video_interviews_page.html', key='video_interviews_page')
def collateral(request, template='resources/collateral.html', extra_context=None):
    context = init_mode(request)

    video_iconsensus = VideoIconsensus.objects.all().order_by('-video_iconsensus_date')
    for url in video_iconsensus:
        url.video_iconsensus_link = url.video_iconsensus_link.replace("watch?v=", "embed/")+"?rel=0"

    video_events = VideoEvents.objects.all().order_by('-video_events_date')
    for url in video_events:
        url.video_events_link = url.video_events_link.replace("watch?v=", "embed/")+"?rel=0"

    video_interviews = VideoInterviews.objects.all().order_by('-video_interviews_date')
    for url in video_interviews:
        url.video_interviews_link = url.video_interviews_link.replace("watch?v=", "embed/")+"?rel=0"

    context.update({
        'video_iconsensus': video_iconsensus,
        'video_events': video_events,
        'video_interviews': video_interviews,
        'subsection': 'COLLATERAL',
    })

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@page_template('resources/news_page.html', key='news_page')
@page_template('resources/press_page.html', key='press_page')
def press(request, template='resources/press.html', extra_context=None):
    context = init_mode(request)
    context.update({
        'news': News.objects.all().order_by('-news_date'),
        'presses': Press.objects.all().order_by('-press_date'),
        'subsection': 'PRESS',
    })

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
