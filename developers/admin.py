from django.contrib import admin
from .models import BlogTutorial, VideoTutorial, VideoPresentation, RewardCalculator, SCORE

admin.site.register(BlogTutorial)
admin.site.register(VideoTutorial)
admin.site.register(VideoPresentation)
admin.site.register(RewardCalculator)
admin.site.register(SCORE)
