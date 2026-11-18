"""
Views for the tracker application.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.db import IntegrityError, transaction
from .forms import RegisterForm

def index(request):
    """
    Root endpoint. Redirects authenticated users to the dashboard and
    unauthenticated visitors to the login page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def register_view(request):
    """
    Handles user registration. Authenticated users are redirected to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
            except IntegrityError:
                form.add_error('username', "A user with that username already exists.")
                return render(request, 'registration/register.html', {'form': form})
            login(request, user)
            messages.success(request, f"Welcome to Expense Tracker, {user.username}!")
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
