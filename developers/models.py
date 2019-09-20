from django.db import models

import datetime
from django.utils.translation import gettext as _


class BlogTutorial(models.Model):
    blog_tutorial_logo = models.ImageField(upload_to='blogtutorial/')
    blog_tutorial_title = models.CharField(max_length=2000, default='')
    blog_tutorial_link = models.URLField(max_length=500, default='')
    blog_tutorial_date = models.DateField(_("Date"), default=datetime.date.today)
    blog_tutorial_display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog_tutorial_title


class VideoTutorial(models.Model):
    video_tutorial_title = models.CharField(max_length=2000, default='')
    video_tutorial_link = models.URLField(max_length=500, default='')
    video_tutorial_date = models.DateField(_("Date"), default=datetime.date.today)
    video_tutorial_display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_tutorial_title


class VideoPresentation(models.Model):
    video_presentation_title = models.CharField(max_length=2000, default='')
    video_presentation_link = models.URLField(max_length=500, default='')
    video_presentation_date = models.DateField(_("Date"), default=datetime.date.today)
    video_presentation_display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_presentation_title


class RewardCalculator(models.Model):
    rc_logo = models.ImageField(upload_to='rewardcalculator/')
    rc_logo_w = models.ImageField(upload_to='rewardcalculator/')
    rc_title = models.CharField(max_length=100, default='')
    rc_link = models.URLField(max_length=500, default='')
    rc_category = models.CharField(max_length=50, default='')
    rc_description = models.TextField(max_length=2000, default='')
    rc_date = models.DateField(_("Date"), default=datetime.date.today)
    display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.rc_title


class SCORE(models.Model):
    score_logo = models.ImageField(upload_to='score/')
    score_logo_w = models.ImageField(upload_to='score/')
    score_title = models.CharField(max_length=100, default='')
    score_link = models.URLField(max_length=500, default='')
    score_category = models.CharField(max_length=50, default='')
    score_description = models.TextField(max_length=2000, default='')
    score_date = models.DateField(_("Date"), default=datetime.date.today)
    display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.score_title
