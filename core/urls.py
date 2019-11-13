from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('dashboard.urls')),
    path('prep/', include('prep.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('iconsensus/', include('iconsensus.urls')),
    path('resources/', include('resources.urls')),
    path('developers/', include('developers.urls')),
    path('dapps/', include('dapps.urls')),
    path('admin/', admin.site.urls),
    path('toggle_nightmode/', views.toggle_nightmode, name='toggle_nightmode'),
    path('toggle_navbar/', views.toggle_navbar, name='toggle_navbar'),
    path('set_wallet/<str:fromAddress>/', views.set_wallet, name='set_wallet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
