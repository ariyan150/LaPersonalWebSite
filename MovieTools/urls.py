from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('parentsguide/', views.parents_guide),
    path('morelike/', views.more_like),
    path('top/<int:genre_id>/', views.top),
    path('top/<str:genre_name>/', views.top_by_genre),
    path('parentsguide/<str:imdb_id>/<str:movie_name>/', views.parents_guide),
    path('morelike/<str:imdb_id>/<str:movie_name>/', views.more_like),
    path('trailer/<str:movie_name>/', views.trailer),
]