from django.shortcuts import render, redirect
from .models import TopMovie, Genre
import requests
import json
from nltk.tokenize import wordpunct_tokenize
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

headers = {
        'x-rapidapi-key': "ea4ba8f6aamsh23ffbbac2f6a618p1bd384jsna311b8e29f36",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }


def index(response):
    return render(response, 'MovieTools/index.html')


def parents_guide(response, imdb_id='...', movie_name='...'):
    filter_list = ['nude', 'nudity', 'frontal', 'sex']
    reviews = []
    url = "https://imdb8.p.rapidapi.com/title/get-parental-guide"
    error = False
    
    if response.method == 'POST':
        if response.POST.get('id'):
            try:
                imdb_id = response.POST.get('id')
                querystring = {"tconst": imdb_id}
                data = requests.request("GET", url, headers=headers, params=querystring).json()
            except:
                error = True 
    elif imdb_id != '...':
        querystring = {"tconst": imdb_id}
        data = requests.request("GET", url, headers=headers, params=querystring).json()

    if error:
            messages.error(response, 'Please Search again')
    else:
        try:
            lists = data["parentalguide"]
            for x in lists:
                for y in x['items']:
                    text = wordpunct_tokenize(y['text'])
                    for word in filter_list:   
                        if  word in text:
                            reviews.append(y['text'])
                            break
        except:
            pass
    
    if len(reviews) == 0:
            messages.error(response, 'No Result for this movie')

    return render(response, 'MovieTools/parents_guide.html', {'reviews': reviews, 'imdb_id': imdb_id, 'movie_name':movie_name})


def more_like(response, imdb_id='...', movie_name='...'):
    movies = []
    if response.method == 'POST':
        if response.POST.get('id'):
            imdb_id = response.POST.get('id')

    if imdb_id != '...':
        try:
            url = "https://imdb8.p.rapidapi.com/title/get-more-like-this"
            querystring = {"tconst": imdb_id,"currentCountry":"US","purchaseCountry":"US"}
            data = requests.request("GET", url, headers=headers, params=querystring).json()
            
            for x in data:
                movie_id = x.split('/')[-2]
                url = f"http://www.omdbapi.com/?i={movie_id}&apikey=af3d009a"
                movie = requests.get(url).json()
                movie = {'Title':f"{movie['Title']} ({movie['Year']})", 'img':movie['Poster'], 'imdbID':movie['imdbID']}
                movies.append(movie)
        except:
            pass

    return render(response, 'MovieTools/more_like.html', {'movies':movies, 'imdb_id':imdb_id, 'movie_name':movie_name})


def trailer(response, movie_name):
    url = "https://youtube-search-results.p.rapidapi.com/youtube-search/"
    querystring = {"q":f"{movie_name}+trailer"}
    headers = {
        'x-rapidapi-key': "ea4ba8f6aamsh23ffbbac2f6a618p1bd384jsna311b8e29f36",
        'x-rapidapi-host': "youtube-search-results.p.rapidapi.com"
        }
    data = requests.request("GET", url, headers=headers, params=querystring).json()
    youtube_id = []

    print(movie_name, '\n', data)

    count = 0
    for item in data['items']:
        if item['type'] == 'video':
            youtube_id.append(item['id'])
            count += 1

        if count == 4:
            break

    return render(response, 'MovieTools/trailer.html', {'movie_name':movie_name, 'youtube_id':youtube_id})


def top(response, genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
    except:
        messages.error(response, "This Url Dosn't Exist")
        return redirect('/movietools')

    if response.method == 'POST':
        if response.POST.get('update'):
            TopMovie.objects.filter(genre_id=genre_id).delete()

            if genre_id == 1:
                url = "https://imdb8.p.rapidapi.com/title/get-most-popular-movies"
                querystring = {"purchaseCountry":"US","homeCountry":"US","currentCountry":"US"}
                data = requests.request("GET", url, headers=headers, params=querystring).json()

                count = 1
                for item in data:
                    imdb_id = item.split('/')[-2]
                    print(imdb_id)
                    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=af3d009a"
                    movie = requests.get(url).json()
                    newMovie = TopMovie(genre_id=genre_id, name=movie['Title'], year=movie['Year'], imdb_id=movie['imdbID'],
                                        metascore= movie['Metascore'], img_url=movie['Poster'], director=movie['Director'],
                                        imdbRating=movie['imdbRating'], number=count)
                    newMovie.save()
                    count += 1
            elif genre_id == 3:
                url = "https://imdb8.p.rapidapi.com/title/get-top-rated-movies"
                data = requests.request("GET", url, headers=headers).json()

                count = 1
                for item in data:
                    imdb_id = item['id'].split('/')[-2]
                    print(imdb_id)
                    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=af3d009a"
                    movie = requests.get(url).json()
                    newMovie = TopMovie(genre_id=genre_id, name=movie['Title'], year=movie['Year'], imdb_id=movie['imdbID'],
                                        metascore= movie['Metascore'], img_url=movie['Poster'], director=movie['Director'],
                                        imdbRating=movie['imdbRating'], number=count)
                    newMovie.save()
                    count += 1
            elif genre_id == 4:
                url = "https://imdb8.p.rapidapi.com/title/get-most-popular-tv-shows"
                querystring = {"purchaseCountry":"US","currentCountry":"US","homeCountry":"US"}
                data = requests.request("GET", url, headers=headers, params=querystring).json()
                count = 1
                for item in data:
                    imdb_id = item.split('/')[-2]
                    print(imdb_id)
                    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=af3d009a"
                    movie = requests.get(url).json()
                    newMovie = TopMovie(genre_id=genre_id, name=movie['Title'], year=movie['Year'], imdb_id=movie['imdbID'],
                                        metascore= movie['Metascore'], img_url=movie['Poster'], director=movie['Director'],
                                        imdbRating=movie['imdbRating'], number=count)
                    newMovie.save()
                    count += 1


    top_list = TopMovie.objects.filter(genre_id=genre_id)
 
    page = response.GET.get('page', 1)
    paginator = Paginator(top_list, 20)
    try:
        top_list = paginator.page(page)
    except PageNotAnInteger:
        top_list = paginator.page(1)
    except EmptyPage:
        top_list = paginator.page(paginator.num_pages)

    return render(response, 'MovieTools/top_movies.html', {'top_list':top_list, 'genre_id':genre_id})


def top_by_genre(response, genre_name):
    try:
        genre = Genre.objects.get(name=genre_name)
    except:
        messages.error(response, "This Url Dosn't Exist")
        return redirect('/movietools')

    if response.method == 'POST':
        url = "https://imdb8.p.rapidapi.com/title/get-popular-movies-by-genre"
        querystring = {"genre":f"/chart/popular/genre/{genre_name}"}
        data = requests.request("GET", url, headers=headers, params=querystring).json()

        if response.POST.get('update'):
            TopMovie.objects.filter(genre_id=genre.id).delete()
            count = 1
            for item in data:
                imdb_id = item.split('/')[-2]
                print(imdb_id)
                url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=af3d009a"
                movie = requests.get(url).json()
                newMovie = TopMovie(genre_id=genre.id, name=movie['Title'], year=movie['Year'], imdb_id=movie['imdbID'],
                                    metascore= movie['Metascore'], img_url=movie['Poster'], director=movie['Director'],
                                    imdbRating=movie['imdbRating'], number=count)
                newMovie.save()
                count += 1


    top_list = TopMovie.objects.filter(genre_id=genre.id)
 
    page = response.GET.get('page', 1)
    paginator = Paginator(top_list, 20)
    try:
        top_list = paginator.page(page)
    except PageNotAnInteger:
        top_list = paginator.page(1)
    except EmptyPage:
        top_list = paginator.page(paginator.num_pages)

    return render(response, 'MovieTools/top_by_genre.html', {'top_list':top_list, 'genre':genre.name})