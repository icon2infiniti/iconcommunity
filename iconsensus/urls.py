from django.urls import path

from . import views

urlpatterns = [
    path('overview/', views.overview, name='overview'),
    path('about/', views.about, name='about'),
    path('candidates/', views.candidates, name='candidates'),
    path('prep_projects/create', views.prep_project_create, name='prep_project_create'),
    path('prep_projects/<int:id>/edit', views.prep_project_edit, name='prep_project_edit'), 
    path('prep_projects/<int:id>/', views.prep_project, name='prep_project'),    
    path('prep_projects/<str:prep_address>', views.prep_projects, name='prep_projects'),
    path('prep_all_projects/', views.prep_all_projects, name='prep_all_projects'),
    path('candidate_detail/<int:pk>/', views.candidate_detail, name='candidate_detail'),
]
