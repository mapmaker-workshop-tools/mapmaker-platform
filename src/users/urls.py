"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


from users import views


urlpatterns = [
    path('login', views.login_user, name='login'),
    path('profile', views.profile, name='user profile'),
    path('profile/<int:id>/edit', views.profile_edit, name='user profile'),
    path('logout', views.logout_view, name='logout'),
    path('<int:id>/delete', views.delete_user, name='user delete'),
    path('register/<str:workshop_secret>', views.register, name='register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_email.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_completed.html'), name="password_reset_complete"),
]
