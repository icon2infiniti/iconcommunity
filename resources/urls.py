from django.urls import path

from . import views

urlpatterns = [
    path('collateral/', views.collateral, name='collateral'),
    path('links/', views.links, name='links'),
    #path('press/', views.press, name='press'),
    #path('news/', views.news, name='news'),
]
