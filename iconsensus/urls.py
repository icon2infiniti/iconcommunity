from django.urls import path
from . import views

from .api import (
    PrepProjectsAPI,
    PrepProjectAPI,
    PrepProjectFiltersApi,
    PrepApi,
    PrepFiltersApi,
)

urlpatterns = [
    path('overview/', views.overview, name='overview'),
    path('about/', views.about, name='about'),
    path('candidates/', views.candidates, name='candidates'),
    path('prep_projects/create', views.prep_project_create, name='prep_project_create'),
    path('prep_projects/<int:id>/edit', views.prep_project_edit, name='prep_project_edit'), 
    path('prep_projects/<int:id>/', views.prep_project, name='prep_project'),    
    path('prep_projects/<str:prep_address>', views.prep_projects, name='prep_projects'),
    path('candidate_detail/<int:pk>/', views.candidate_detail, name='candidate_detail'),
]


# API ENDPOINTS
urlpatterns += [
    path('api/prep-projects/', PrepProjectsAPI.as_view(), name="api_prep_projects"),
    path('api/prep-projects/<int:pk>/', PrepProjectAPI.as_view(), name="api_prep_project"),
    path('api/prep-projects/filters/', PrepProjectFiltersApi.as_view({ 'get': 'get', }), name="api_prep_project_filters"),
    path('api/prep/filters/', PrepFiltersApi.as_view({ 'get': 'get', }), name="api_prep_filters"),    
    path('api/prep/<str:prep_address>/', PrepApi.as_view({ 'get': 'get', }), name="api_preps"),
]
