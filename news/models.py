from django.db import models


class Tweet(models.Model):
    twitter_id = models.CharField(max_length=100, default='')
    thumb = models.URLField(max_length=500, default='')
    author = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField()
    content = models.CharField(max_length=500, default='')
    url = models.URLField(max_length=500, default='')
    retweet = models.IntegerField()
    likes = models.IntegerField()
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Reddit(models.Model):
    thumbnail = models.CharField(max_length=500, default='')
    author = models.CharField(max_length=100, default='')
    created = models.FloatField()
    title = models.CharField(max_length=500, default='')
    url = models.URLField(max_length=500, default='')
    score = models.IntegerField()
    num_comments = models.IntegerField()
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Iconist(models.Model):
    thumb = models.CharField(max_length=500, default='')
    author = models.CharField(max_length=100, default='')
    published = models.DateTimeField()
    link = models.URLField(max_length=500, default='')
    title = models.CharField(max_length=500, default='')
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title