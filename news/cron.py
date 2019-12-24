from .models import Tweet, Reddit, Iconist
from dateutil.parser import parse
import tweepy
import praw
import feedparser
from bs4 import BeautifulSoup


def latest_tweets():
    print("Tweet!")

    #Twitter
    MAX_TWEETS = 20
    auth = tweepy.OAuthHandler("sq3iEj5FrRHtuZdHG209GNhNX", "it8cSeHYGPPB6pegyzgKUr9rZ4pT05NJVnQM0d3g5cpxTYdffx")
    api = tweepy.API(auth)
    twitter_entries = [status._json for status in tweepy.Cursor(api.search,  q='#ICONProject -filter:retweets').items(MAX_TWEETS)]

    Tweet.objects.all().delete()
    for entry in twitter_entries:
        tweet = Tweet()
        tweet.twitter_id = entry['id']
        tweet.thumb = entry['user']['profile_image_url_https']
        tweet.author = entry['user']['screen_name']
        tweet.created_at = parse(entry['created_at'])
        tweet.content = entry['text']
        tweet.url = 'https://twitter.com/'+entry['user']['screen_name']+'/status/'+str(entry['id'])
        tweet.retweet = entry['retweet_count']
        tweet.likes = entry['favorite_count']
        tweet.save()
        print('thumb: '+tweet.thumb)
        print('author: ' + tweet.author)
        print('created_at: ' + str(tweet.created_at))
        print('content: ' + tweet.content)
        print('url: ' + tweet.url)
        print('retweet: ' + str(tweet.retweet))
        print('likes: ' + str(tweet.likes))
        print('queried_at: ' + str(tweet.queried_at))


def latest_reddits():
    print("Reddit!")

    reddit = praw.Reddit(client_id='GYqmrmi5cunm1A',
                         client_secret='rydmYFNqBKpnwkvjwybmfNzSY-g',
                         user_agent='icon.community')

    reddit_entries = reddit.subreddit('helloicon').hot(limit=20)\

    Reddit.objects.all().delete()
    for entry in reddit_entries:
        reddit = Reddit()
        reddit.thumbnail = entry.thumbnail
        reddit.author = str(entry.author)
        reddit.created = entry.created
        reddit.title = entry.title
        reddit.url = entry.url
        reddit.score = entry.score
        reddit.num_comments = entry.num_comments
        reddit.save()
        print('thumb: '+reddit.thumbnail)
        print('author: ' + reddit.author)
        print('created: ' + str(reddit.created))
        print('title: ' + reddit.title)
        print('url: ' + reddit.url)
        print('score: ' + str(reddit.score))
        print('num_comments: ' + str(reddit.num_comments))


def latest_iconists():
    print("Iconist!")

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
        iconist.published = parse(entry['published'])
        iconist.link = entry.link
        iconist.title = entry.title
        iconist.save()
        print('thumb: '+iconist.thumb)
        print('author: ' + iconist.author)
        print('published: ' + str(iconist.published))
        print('link: ' + iconist.link)
        print('title: ' + iconist.title)
