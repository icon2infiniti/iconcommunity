from django.db import models


class DailyTransactions(models.Model):
    targetDate = models.CharField(max_length=20, default='')
    txCount = models.IntegerField()
    tx24h = models.IntegerField(default=0)

    def __str__(self):
        return str(self.targetDate)


class WalletCount(models.Model):
    selectDate = models.CharField(max_length=20, default='')
    totalCount = models.IntegerField()
    balanceCount = models.IntegerField()

    def __str__(self):
        return str(self.selectDate)


class RewardRate(models.Model):
    total_delegation = models.FloatField()
    total_supply = models.FloatField()
    circ_supply = models.FloatField()
    transactionCount = models.IntegerField()
    publicTreasury = models.FloatField()
    create_day = models.DateField()

    def __str__(self):
        return str(self.create_day)


class Top20Wallets(models.Model):
    t20json = models.CharField(max_length=5000)
    query_date = models.DateTimeField(auto_now=True)


class MainInfo(models.Model):
    maininfo_json = models.CharField(max_length=1000)
    query_date = models.DateTimeField(auto_now=True)


class TopDapps(models.Model):
    topdapps_json = models.CharField(max_length=5000)
    tx = models.IntegerField()
    vol = models.FloatField()
    fee = models.FloatField()
    icx_price = models.FloatField()
    create_day = models.DateField()

    def __str__(self):
        return str(self.create_day)


class SocialInfo(models.Model):
    average_sentiment_calc_24h = models.FloatField()
    average_sentiment_calc_24h_percent = models.FloatField()
    social_score_calc_24h = models.FloatField()
    social_score_calc_24h_percent = models.FloatField()
    social_volume_calc_24h = models.FloatField()
    social_volume_calc_24h_percent = models.FloatField()
    create_day = models.DateField()

    def __str__(self):
        return str(self.create_day)