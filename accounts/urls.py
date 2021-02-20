from django.contrib import admin
from django.urls import path
from .views import emailVerification
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register, name='register'),
    path('activate/<uidb64>/<token>',emailVerification.as_view(), name='activate'),
    path('accounts/login/',views.login_view, name='login'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"), name='password_reset_complete'),
    path('logout/', views.logout_view, name='logout_view'),
]
