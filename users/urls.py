from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register-student/', views.lecturer_register_student_view, name='register_student'),
    path('register-lecturer/', views.admin_register_lecturer_view, name='register_lecturer'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
