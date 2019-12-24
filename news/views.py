from django.shortcuts import render
from news.cron import latest_tweets, latest_reddits, latest_iconists, latest_mediums
from .models import Tweet, Reddit, Iconist, Medium

#import feedparser
#from bs4 import BeautifulSoup

#from dateutil.parser import parse
#import tweepy
#import praw


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

    latest_tweets()
    latest_reddits()
    latest_iconists()
    latest_mediums()

    '''
    MEDIUM = feedparser.parse('https://medium.com/feed/helloiconworld')
    medium_entries = MEDIUM['entries']
    for entry in medium_entries:
        soup = BeautifulSoup(entry['content'][0]['value'], 'html.parser')
        imgtag = soup.find('img')
        if imgtag:
            entry['thumb'] = imgtag['src']

    THEICONIST = feedparser.parse('https://theicon.ist/feed/')
    theiconist_entries = THEICONIST['entries']
    for entry in theiconist_entries:
        soup = BeautifulSoup(entry['content'][0]['value'], 'html.parser')
        imgtag = soup.find('img')
        if imgtag:
            entry['thumb'] = imgtag['src']
    '''

    #Twitter
    '''
    MAX_TWEETS = 1
    auth = tweepy.OAuthHandler("sq3iEj5FrRHtuZdHG209GNhNX", "it8cSeHYGPPB6pegyzgKUr9rZ4pT05NJVnQM0d3g5cpxTYdffx")
    api = tweepy.API(auth)
    twitter_entries = [status._json for status in tweepy.Cursor(api.search,  q='#ICONProject -filter:retweets').items(MAX_TWEETS)]

    for dt in twitter_entries:
        dt['created_at'] = parse(dt['created_at'])
    '''

    twitter_entries = Tweet.objects.all()
    reddit_entries = Reddit.objects.all()
    medium_entries = Medium.objects.all()
    iconist_entries = Iconist.objects.all()

    #Reddit
    '''
    reddit = praw.Reddit(client_id='GYqmrmi5cunm1A',
                         client_secret='rydmYFNqBKpnwkvjwybmfNzSY-g',
                         user_agent='icon.community')

    reddit_entries = reddit.subreddit('helloicon').hot(limit=10)
    '''

    #TheICONist
    '''
    THEICONIST = feedparser.parse('https://theicon.ist/feed/')
    theiconist_entries = THEICONIST['entries']
    for entry in theiconist_entries:
        entry['published'] = parse(entry['published'])
        soup = BeautifulSoup(entry['content'][0]['value'], 'html.parser')
        imgtag = soup.find('img')
        if imgtag:
            entry['thumb'] = imgtag['src']
    '''

    context.update({
        'subsection': 'NEWS',
        'twitter_entries': twitter_entries,
        'reddit_entries': reddit_entries,
        'medium_entries': medium_entries,
        'iconist_entries': iconist_entries,
    })

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

