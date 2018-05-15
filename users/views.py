# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProfileForm
from .models import User

# Create your views here.

def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})

def index(request):
    return render(request, 'users/index.html')

def profile(request, pk):
    user=get_object_or_404(User, pk=pk)
    form = ProfileForm(instance=user)
    return render(request, 'users/profile.html', context={'form': form})
