from django.db import models

import datetime
from django.utils.translation import gettext as _


class News(models.Model):
    news_logo = models.ImageField(upload_to='news/')
    news_site = models.CharField(max_length=200, default='')
    news_title = models.CharField(max_length=2000, default='')
    news_link = models.URLField(max_length=500, default='')
    news_date = models.DateField(_("Date"), default=datetime.date.today)
    news_display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.news_title


class Press(models.Model):
    press_title = models.CharField(max_length=2000, default='')
    press_link = models.URLField(max_length=500, default='')
    press_date = models.DateField(_("Date"), default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.press_title


class Video(models.Model):
    video_title = models.CharField(max_length=2000, default='')
    video_link = models.URLField(max_length=2000, default='')
    video_date = models.DateField(_("Date"), default=datetime.date.today)
    video_category = models.CharField(max_length=2000, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_title


class VideoIconsensus(models.Model):
    video_iconsensus_title = models.CharField(max_length=2000, default='')
    video_iconsensus_link = models.URLField(max_length=2000, default='')
    video_iconsensus_date = models.DateField(_("Date"), default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_iconsensus_title


class VideoEvents(models.Model):
    video_events_title = models.CharField(max_length=2000, default='')
    video_events_link = models.URLField(max_length=2000, default='')
    video_events_date = models.DateField(_("Date"), default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_events_title


class VideoInterviews(models.Model):
    video_interviews_title = models.CharField(max_length=2000, default='')
    video_interviews_link = models.URLField(max_length=2000, default='')
    video_interviews_date = models.DateField(_("Date"), default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_interviews_title

