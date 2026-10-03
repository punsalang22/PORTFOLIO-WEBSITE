from django.urls import path
from . import views

urlpatterns = [
    path('', views.personal_info, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('personal/', views.personal_info, name='personal_info'),
]