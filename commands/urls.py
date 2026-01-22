from django.urls import path
from . import views

urlpatterns = [
    path('', views.command_list, name='command_list'),
    path('command/<int:pk>/', views.command_detail, name='command_detail'),
    path('add/', views.add_command, name='add_command'),
    path('command/<int:pk>/suggest/', views.suggest_edit, name='suggest_edit'),
    path('command/<int:pk>/edit/', views.edit_command, name='edit_command'),
    path('review/<int:pk>/', views.review_edit, name='review_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]
