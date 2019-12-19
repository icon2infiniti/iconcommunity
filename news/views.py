from django.shortcuts import render

#import feedparser
#from bs4 import BeautifulSoup

#from datetime import datetime
from dateutil.parser import parse
import tweepy
import praw


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

    '''
    REDDIT = feedparser.parse('https://reddit.com/r/helloicon.rss')
    reddit_entries = REDDIT['entries'][0:10]
    for entry in reddit_entries:
        soup = BeautifulSoup(entry['content'][0]['value'], 'html.parser')
        imgtag = soup.find('img')
        if imgtag:
            entry['thumb'] = imgtag['src']
        entry['author'] = entry['author'][3:len(entry['author'])]
        entry['updated'] = parse(entry['updated'])
    '''

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
    MAX_TWEETS = 10
    auth = tweepy.OAuthHandler("sq3iEj5FrRHtuZdHG209GNhNX", "it8cSeHYGPPB6pegyzgKUr9rZ4pT05NJVnQM0d3g5cpxTYdffx")
    api = tweepy.API(auth)
    twitter_entries = [status._json for status in tweepy.Cursor(api.search,  q='#ICONProject -filter:retweets').items(MAX_TWEETS)]

    for dt in twitter_entries:
        dt['created_at'] = parse(dt['created_at'])

    # Reddit
    reddit = praw.Reddit(client_id='GYqmrmi5cunm1A',
                         client_secret='rydmYFNqBKpnwkvjwybmfNzSY-g',
                         user_agent='icon.community')

    reddit_entries = reddit.subreddit('helloicon').hot(limit=10)

    '''
    for submission in submissions:
        print(submission.title)  # Output: the submission's title
        print(submission.score)  # Output: the submission's score
        print(submission.id)  # Output: the submission's ID
        print(submission.url)  # Output: the URL the submission points to
        print(submission.num_comments)
    '''

    context.update({
        'subsection': 'NEWS',
        'reddit_entries': reddit_entries,
        #'medium_entries': medium_entries,
        #'theiconist_entries': theiconist_entries,
        'twitter_entries': twitter_entries,
    })

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

