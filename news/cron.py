from .models import Tweet, Reddit, Iconist, Medium, YouTube, Rhizome
from dateutil.parser import parse
import tweepy
import praw
import feedparser
from bs4 import BeautifulSoup
import requests
from isodate import parse_duration
import datetime


def latest_tweets():
    print("Tweet: "+str(datetime.datetime.now()))

    #Twitter
    MAX_TWEETS = 20
    auth = tweepy.OAuthHandler("sq3iEj5FrRHtuZdHG209GNhNX", "it8cSeHYGPPB6pegyzgKUr9rZ4pT05NJVnQM0d3g5cpxTYdffx")
    api = tweepy.API(auth)
    twitter_entries = [status._json for status in tweepy.Cursor(api.search, tweet_mode='extended', q='#ICONProject -filter:retweets -from:ICXshark').items(MAX_TWEETS)]

    Tweet.objects.all().delete()
    for entry in twitter_entries:
        tweet = Tweet()
        tweet.twitter_id = entry['id']
        tweet.thumb = entry['user']['profile_image_url_https']
        tweet.author = entry['user']['screen_name']
        tweet.created_at = parse(entry['created_at'])
        tweet.content = entry['full_text']
        tweet.url = 'https://twitter.com/'+entry['user']['screen_name']+'/status/'+str(entry['id'])
        tweet.retweet = entry['retweet_count']
        tweet.likes = entry['favorite_count']
        tweet.save()
        '''
        print('thumb: '+tweet.thumb)
        print('author: ' + tweet.author)
        print('created_at: ' + str(tweet.created_at))
        print('content: ' + tweet.content)
        print('url: ' + tweet.url)
        print('retweet: ' + str(tweet.retweet))
        print('likes: ' + str(tweet.likes))
        print('queried_at: ' + str(tweet.queried_at))
        '''


def latest_reddits():
    print("Reddit: "+str(datetime.datetime.now()))

    reddit = praw.Reddit(client_id='GYqmrmi5cunm1A',
                         client_secret='rydmYFNqBKpnwkvjwybmfNzSY-g',
                         user_agent='icon.community')

    reddit_entries = reddit.subreddit('helloicon').hot(limit=20)\

    Reddit.objects.all().delete()
    for entry in reddit_entries:
        reddit = Reddit()
        reddit.thumbnail = entry.thumbnail
        reddit.author = str(entry.author)
        reddit.created_at = datetime.datetime.utcfromtimestamp(entry.created_utc)
        reddit.title = entry.title
        reddit.url = entry.url
        reddit.score = entry.score
        reddit.num_comments = entry.num_comments
        reddit.save()
        '''
        print('thumb: '+reddit.thumbnail)
        print('author: ' + reddit.author)
        print('created: ' + str(reddit.created))
        print('title: ' + reddit.title)
        print('url: ' + reddit.url)
        print('score: ' + str(reddit.score))
        print('num_comments: ' + str(reddit.num_comments))
        '''


def latest_iconists():
    print("Iconist: "+str(datetime.datetime.now()))

    THEICONIST = feedparser.parse('https://theicon.ist/feed/')
    theiconist_entries = THEICONIST['entries']

    Iconist.objects.all().delete()
    for entry in theiconist_entries:
        iconist = Iconist()
        soup = BeautifulSoup(entry['content'][0]['value'], 'html.parser')
        imgtag = soup.find('img')
        if imgtag:
            iconist.thumb = imgtag['src']
        iconist.author = entry.author
        iconist.created_at = parse(entry['published'])
        iconist.link = entry.link
        iconist.title = entry.title
        iconist.save()
        '''
        print('thumb: '+iconist.thumb)
        print('author: ' + iconist.author)
        print('published: ' + str(iconist.published))
        print('link: ' + iconist.link)
        print('title: ' + iconist.title)
        '''


def latest_mediums():
    print("Medium: "+str(datetime.datetime.now()))

    MEDIUM = feedparser.parse('https://medium.com/feed/helloiconworld')
    medium_entries = MEDIUM['entries']

    Medium.objects.all().delete()
    for entry in medium_entries:
        medium = Medium()
        soup = BeautifulSoup(entry['content'][0]['value'], 'html.parser')
        imgtag = soup.find('img')
        if imgtag:
            medium.thumb = imgtag['src']
        medium.author = entry.author
        medium.category = entry.category
        medium.created_at = parse(entry['published'])
        medium.link = entry.link
        medium.title = entry.title
        medium.save()
        '''
        print('thumb: '+medium.thumb)
        print('creator: ' + medium.author)
        print('category: ' + medium.category)
        print('published: ' + str(medium.published))
        print('link: ' + medium.link)
        print('title: ' + medium.title)
        '''

'''
def latest_youtubes():
    print("YouTube: "+str(datetime.datetime.now()))

    YOUTUBE_KEY = 'AIzaSyCE_5nBlyA8-mUfUh661k0AOfSbd5EhZeo'
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part': 'snippet',
        'q': 'ICON ICX',
        'key': YOUTUBE_KEY,
        'maxResults': 10,
        'type': 'video',
    }
    r = requests.get(search_url, params=search_params)
    #print(r.json())
    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])


    video_params = {
        'key': YOUTUBE_KEY,
        'part': 'snippet,contentDetails',
        'id': ','.join(video_ids),
        'maxResults': 10
    }
    r = requests.get(video_url, params=video_params)
    youtube_entries = r.json()['items']

    YouTube.objects.all().delete()
    for entry in youtube_entries:
        youtube = YouTube()
        youtube.youtube_id = entry['id']
        youtube.title = entry['snippet']['title']
        youtube.created_at = parse(entry['snippet']['publishedAt'])
        youtube.duration = int(parse_duration(entry['contentDetails']['duration']).total_seconds()//60)
        youtube.thumb = entry['snippet']['thumbnails']['default']['url']
        youtube.author = entry['snippet']['channelTitle']
        youtube.save()
'''


def latest_rhizomes():
    print("Rhizome: "+str(datetime.datetime.now()))

    RHIZOME = feedparser.parse('https://rhizomewire.substack.com/feed')
    rhizome_entries = RHIZOME['entries']

    Rhizome.objects.all().delete()
    for entry in rhizome_entries:
        rhizome = Rhizome()
        rhizome.created_at = parse(entry['published'])
        rhizome.link = entry.link
        rhizome.title = entry.title
        rhizome.save()


def news_cron_15m():
    latest_tweets()
    latest_reddits()


def news_cron_6h():
    latest_iconists()
    latest_mediums()
    #latest_youtubes()
    latest_rhizomes()
