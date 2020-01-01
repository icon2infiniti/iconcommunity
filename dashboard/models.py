from django.db import models


class DailyTransactions(models.Model):
    targetDate = models.CharField(max_length=20, default='')
    txCount = models.IntegerField()

    def __str__(self):
        return str(self.targetDate)