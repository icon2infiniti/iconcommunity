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
    #publish_on = models.DateField()

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