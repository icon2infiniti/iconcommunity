from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('management/', views.management, name='management'),
    path('governance/', views.governance, name='governance'),
    path('proposal/', views.proposal, name='proposal'),
]