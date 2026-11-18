"""
URL configuration for the tracker application.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        form_class=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
