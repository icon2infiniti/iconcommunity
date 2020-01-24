from django.shortcuts import render
from .models import Tweet, Reddit, Iconist, Medium, YouTube, Rhizome
import datetime
from datetime import timedelta

from news.cron import news_cron_15m, news_cron_6h

from itertools import chain
from operator import attrgetter


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

    today = datetime.datetime.now()
    long_ago = today + timedelta(days=-30)

    news_cron_15m()
    news_cron_6h()
    #latest_tweets()
    #latest_reddits()
    #latest_iconists()
    #latest_mediums()
    #latest_youtubes()
    #latest_rhizomes()

    twitter_entries = Tweet.objects.all()
    reddit_entries = Reddit.objects.all()
    youtube_entries = YouTube.objects.filter(created_at__gte=long_ago)
    medium_entries = Medium.objects.filter(created_at__gte=long_ago)
    iconist_entries = Iconist.objects.filter(created_at__gte=long_ago)
    rhizome_entries = Rhizome.objects.filter(created_at__gte=long_ago)

    all_entries = list(chain(twitter_entries, reddit_entries, medium_entries, iconist_entries, rhizome_entries))
    all_entries = sorted(all_entries, key=attrgetter('created_at'), reverse=True)

    context.update({
        'subsection': 'NEWS',
        'all_entries': all_entries,
        'twitter_entries': twitter_entries,
        'reddit_entries': reddit_entries,
        'youtube_entries': youtube_entries,
        'medium_entries': medium_entries,
        'iconist_entries': iconist_entries,
        'rhizome_entries': rhizome_entries,
    })

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

