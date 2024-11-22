from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)
    

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} ({self.rating})"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    movies = models.ManyToManyField(Movie, related_name='tags')

    def __str__(self):
        return self.name
