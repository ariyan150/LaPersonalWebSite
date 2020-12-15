from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie', null=True)
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    imdb_id = models.CharField(max_length=200)
    img_url = models.CharField(max_length=2000)
    director = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    imdbRating = models.CharField(max_length=200)
    metascore = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    added_date = models.DateTimeField(auto_now=True)
    plot = models.TextField(null=True)

    def __str__(self):
        return f'{self.name}({self.year})'

