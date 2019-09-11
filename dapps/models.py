from django.db import models


class TXChallenge(models.Model):
    tx_challenge_logo = models.ImageField(upload_to='dapps/')
    tx_challenge_logo_w = models.ImageField(upload_to='dapps/')
    tx_challenge_title = models.CharField(max_length=100, default='')
    tx_challenge_link = models.URLField(max_length=500, default='')
    tx_challenge_category = models.CharField(max_length=50, default='')
    tx_challenge_description = models.TextField(max_length=2000, default='')
    tx_challenge_author = models.CharField(max_length=50, default='', blank=True)
    display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tx_challenge_title


class OfficialDapps(models.Model):
    official_dapp_logo = models.ImageField(upload_to='dapps/')
    official_dapp_logo_w = models.ImageField(upload_to='dapps/')
    official_dapp_title = models.CharField(max_length=100, default='')
    official_dapp_link = models.URLField(max_length=500, default='')
    official_dapp_category = models.CharField(max_length=50, default='')
    official_dapp_description = models.TextField(max_length=2000, default='')
    tx_challenge_author = models.CharField(max_length=50, default='', blank=True)
    display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.official_dapp_title
