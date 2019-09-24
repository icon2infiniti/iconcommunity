from django.db import models

import datetime
from django.utils.translation import gettext as _


class Tutorial(models.Model):
    tutorial_logo = models.ImageField(upload_to='tutorial/')
    tutorial_title = models.CharField(max_length=2000, default='')
    tutorial_link = models.URLField(max_length=500, default='')
    tutorial_category = models.CharField(max_length=50, default='')
    tutorial_date = models.DateField(_("Date"), default=datetime.date.today)
    tutorial_display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tutorial_title


class MiniCard(models.Model):
    minicard_logo = models.ImageField(upload_to='minicard/')
    minicard_logo_w = models.ImageField(upload_to='minicard/')
    minicard_title = models.CharField(max_length=100, default='')
    minicard_link = models.URLField(max_length=500, default='')
    minicard_category = models.CharField(max_length=50, default='')
    minicard_description = models.TextField(max_length=2000, default='')
    minicard_date = models.DateField(_("Date"), default=datetime.date.today)
    display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.minicard_title
