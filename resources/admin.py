from django.contrib import admin
from .models import News, Press, Video, VideoEvents, VideoInterviews, VideoIconsensus


class CollateralVideo(admin.ModelAdmin):
    list_display = ('video_category', 'video_title')


admin.site.register(News)
admin.site.register(Press)
admin.site.register(Video, CollateralVideo)


admin.site.register(VideoEvents)
admin.site.register(VideoInterviews)
admin.site.register(VideoIconsensus)
