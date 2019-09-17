from django.urls import path

from . import views

urlpatterns = [
    path('', views.dapps, name='dapps'),
]