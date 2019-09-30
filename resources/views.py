from django.shortcuts import render
from .models import News, Press, Video, VideoEvents, VideoInterviews#, VideoIconsensus
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


@page_template('resources/video_general_page.html', key='video_general_page')
@page_template('resources/video_events_page.html', key='video_events_page')
@page_template('resources/video_interviews_page.html', key='video_interviews_page')
def collateral(request, template='resources/collateral.html', extra_context=None):
    context = init_mode(request)

    video_generals = Video.objects.filter(video_category="General").order_by('-video_date')
    for url in video_generals:
        url.video_link = url.video_link.replace("watch?v=", "embed/")+"?rel=0"

    video_events = Video.objects.filter(video_category="Events").order_by('-video_date')
    for url in video_events:
        url.video_link = url.video_link.replace("watch?v=", "embed/")+"?rel=0"

    video_interviews = Video.objects.filter(video_category="Interviews").order_by('-video_date')
    for url in video_interviews:
        url.video_link = url.video_link.replace("watch?v=", "embed/")+"?rel=0"

    context.update({
        'video_generals': video_generals,
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
