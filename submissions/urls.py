from django.urls import path
from . import views

app_name = 'submissions'
urlpatterns = [
    path('editor/', views.editor_view, name='editor'),
    path('list/', views.submission_list_scaffold, name='list_scaffold'),
    path('execute/', views.execute_code_view, name='execute'),
]
