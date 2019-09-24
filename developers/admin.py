from django.contrib import admin
from .models import BlogTutorial, VideoTutorial, VideoPresentation, RewardCalculator, SCORE, Wallet, DB, IDE

admin.site.register(BlogTutorial)
admin.site.register(VideoTutorial)
admin.site.register(VideoPresentation)
admin.site.register(RewardCalculator)
admin.site.register(SCORE)
admin.site.register(Wallet)
admin.site.register(DB)
admin.site.register(IDE)
