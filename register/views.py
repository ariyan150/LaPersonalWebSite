from django.shortcuts import render
from .forms import RegisterForm
from django.contrib import messages


def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, 'Welcome')
    else:
        form = RegisterForm()
    return render(response, 'register/R.html', {'form':form})
