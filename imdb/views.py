from django.shortcuts import render, redirect
import requests
import json
from django.contrib.auth.models import User
from .models import Movie
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def imdb(response):
    movies = []
    if response.method == 'POST':
        if response.POST.get('Search'):
            Searched = response.POST.get('name')
            url = f"http://www.omdbapi.com/?s={Searched}&apikey=af3d009a"
            data = requests.get(url).json()
            if data['Response'] == 'False':
                messages.error(response, 'Please Search again')
            else:
                movies = list(data['Search'])
        if response.POST.get('Add') and response.user.is_authenticated:
            imdb_id = response.POST.get('Add')
            url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=af3d009a"
            movie = requests.get(url).json()
            newMovie = Movie(user=response.user, name=movie['Title'], year=movie['Year'], imdb_id=movie['imdbID'],
                            type=movie['Type'], img_url=movie['Poster'], director=movie['Director'], genre=movie['Genre'],
                            imdbRating=movie['imdbRating'], metascore=movie['Metascore'], time=movie['Runtime'], plot=movie['Plot'])
            newMovie.save()
            messages.success(response, 'Added to your Watchlist')
        elif response.POST.get('Add') and not response.user.is_authenticated:
            messages.error(response, 'Please Login first')

    return render(response, 'imdb/imdb.html', {'movies':movies})


def watchlist(response):
    if response.user.is_authenticated:
        user = response.user
        Movies_list = Movie.objects.filter(user=user)
        if response.POST.get('update'):
            order_info = f"-{response.POST.get('option')}"
            if not response.POST.get('Type') == 'All':
                type_info = response.POST.get('Type')
                Movies_list = Movies_list.filter(type=type_info)
            Movies_list = Movies_list.order_by(order_info)
        elif response.POST.get('Delete'):
            item_id = response.POST.get('Delete')
            select_Item = Movie.objects.get(id=item_id).delete()
        elif response.POST.get('Detail'):
            imdb_id = response.POST.get('Detail')
            return redirect(f'/imdb/detail/{imdb_id}')
        
        page = response.GET.get('page', 1)
        paginator = Paginator(Movies_list, 10)
        try:
            Movies_list = paginator.page(page)
        except PageNotAnInteger:
            Movies_list = paginator.page(1)
        except EmptyPage:
            Movies_list = paginator.page(paginator.num_pages)
    else:
        return redirect('/login')
    return render(response, 'imdb/watchlist.html', {'Movies_list':Movies_list})