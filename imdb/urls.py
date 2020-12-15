from django.urls import path
from . import views

urlpatterns = [
    path('', views.imdb),
    path('watchlist/', views.watchlist),
]