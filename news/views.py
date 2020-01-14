from django.shortcuts import render
from news.cron import news_cron_15m
from news.cron import news_cron_6h
from news.cron import latest_youtubes
from .models import Tweet, Reddit, Iconist, Medium, YouTube
import datetime
from datetime import timedelta


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
    long_ago = today + timedelta(days=-60)

    #news_cron_15m()
    #news_cron_6h()
    #latest_tweets()
    #latest_reddits()
    #latest_iconists()
    #latest_mediums()
    latest_youtubes()

    twitter_entries = Tweet.objects.all().order_by('-created_at')
    reddit_entries = Reddit.objects.all()
    youtube_entries = YouTube.objects.filter(published__gte=long_ago).order_by('-published')
    medium_entries = Medium.objects.filter(published__gte=long_ago)
    iconist_entries = Iconist.objects.filter(published__gte=long_ago)

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

