from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PasswordsChangeView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('reports/', views.reports, name='reports'),
    path('profile/', views.profile, name='profile'),
    path('password_change/', PasswordsChangeView.as_view(), name='password_change'),
]
