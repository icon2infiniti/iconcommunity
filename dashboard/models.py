from django.db import models


class DailyTransactions(models.Model):
    targetDate = models.CharField(max_length=20, default='')
    txCount = models.IntegerField()

    def __str__(self):
        return str(self.targetDate)


class WalletCount(models.Model):
    selectDate = models.CharField(max_length=20, default='')
    #active = models.IntegerField()
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
