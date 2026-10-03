from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.personal_info, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('personal/', views.personal_info, name='personal_info'),

    # Admin/superuser-only area
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/projects/', views.dashboard_projects, name='dashboard_projects'),
    path('dashboard/projects/create/', views.project_create, name='project_create'),
    path('dashboard/tech-stacks/', views.dashboard_tech_stacks, name='dashboard_tech_stacks'),
    path('dashboard/tech-stacks/create/', views.tech_stack_create, name='tech_stack_create'),
]
