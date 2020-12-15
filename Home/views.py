from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def home(response):

    return render(response, 'Home/home.html')