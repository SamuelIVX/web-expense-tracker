"""
Views for the tracker application.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
from .models import Transaction
from .forms import RegisterForm, TransactionForm

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

@login_required
def add_transaction_view(request):
    """
    Renders and processes the expense transaction entry form.
    Associates the newly created transaction with the authenticated user.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_obj = form.save(commit=False)
            transaction_obj.user = request.user
            transaction_obj.save()
            messages.success(
                request,
                f"Added expense: ${transaction_obj.amount:.2f} for {transaction_obj.category.name}."
            )
            return redirect('transaction_history')
    else:
        form = TransactionForm()

    return render(request, 'tracker/add_transaction.html', {'form': form})
