from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TopMovie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='topmovie', null=True)
    number = models.IntegerField()
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    imdb_id = models.CharField(max_length=200)
    img_url = models.CharField(max_length=2000)
    director = models.CharField(max_length=200)
    imdbRating = models.CharField(max_length=200)
    metascore = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.name}({self.year})'
    
    class Meta:
        ordering = ['number']
