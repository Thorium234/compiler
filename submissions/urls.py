from django.urls import path
from . import views

app_name = 'submissions'
urlpatterns = [
    path('editor/<int:assignment_id>/', views.editor_view, name='editor'),
    path('execute/', views.execute_code_view, name='execute'),
    path('submit/<int:assignment_id>/', views.submit_code_view, name='submit'),
]
