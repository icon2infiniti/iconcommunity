from django.shortcuts import render
#from news.cron import latest_tweets, latest_reddits, latest_iconists, latest_mediums, latest_youtubes
from .models import Tweet, Reddit, Iconist, Medium, YouTube


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
        'section': 'NEWS',
    }
    return context


def news(request, template='news/news.html', extra_context=None):
    context = init_mode(request)

    #latest_tweets()
    #latest_reddits()
    #latest_iconists()
    #latest_mediums()
    #latest_youtubes()

    twitter_entries = Tweet.objects.all()
    reddit_entries = Reddit.objects.all()
    youtube_entries = YouTube.objects.all()
    medium_entries = Medium.objects.all()
    iconist_entries = Iconist.objects.all()

    context.update({
        'subsection': 'NEWS',
        'twitter_entries': twitter_entries,
        'reddit_entries': reddit_entries,
        'youtube_entries': youtube_entries,
        'medium_entries': medium_entries,
        'iconist_entries': iconist_entries,
    })

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

