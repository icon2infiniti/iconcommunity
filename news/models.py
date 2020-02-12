from django.db import models

class ICYMI(models.Model):
    author = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=255, default='')
    link = models.URLField()
    create_day = models.DateField()

    def __str__(self):
        return self.author + "- " + self.title


class Tweet(models.Model):
    type = models.CharField(max_length=10, default='tweet')
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
    type = models.CharField(max_length=10, default='reddit')
    thumbnail = models.CharField(max_length=500, default='')
    author = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField()
    title = models.CharField(max_length=500, default='')
    url = models.URLField(max_length=500, default='')
    score = models.IntegerField()
    num_comments = models.IntegerField()
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Iconist(models.Model):
    type = models.CharField(max_length=10, default='iconist')
    thumb = models.CharField(max_length=500, default='')
    author = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField()
    link = models.URLField(max_length=500, default='')
    title = models.CharField(max_length=300, default='')
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Medium(models.Model):
    type = models.CharField(max_length=10, default='medium')
    thumb = models.CharField(max_length=500, default='')
    author = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField()
    link = models.URLField(max_length=500, default='')
    title = models.CharField(max_length=300, default='')
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class YouTube(models.Model):
    type = models.CharField(max_length=10, default='youtube')
    youtube_id = models.CharField(max_length=50, default='')
    thumb = models.URLField(max_length=500, default='')
    title = models.CharField(max_length=500, default='')
    created_at = models.DateTimeField()
    duration = models.IntegerField()
    author = models.CharField(max_length=100, default='')
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Rhizome(models.Model):
    type = models.CharField(max_length=10, default='rhizome')
    created_at = models.DateTimeField()
    link = models.URLField(max_length=500, default='')
    title = models.CharField(max_length=300, default='')
    queried_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title