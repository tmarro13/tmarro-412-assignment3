from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True, null=True, blank=True)  # TMDb ID
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=200, blank=True, null=True)
    release_year = models.PositiveIntegerField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)  # Image from TMDb
    tags = models.ManyToManyField(Tag, related_name="tagged_movies", blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating % 0.5 != 0:
            raise ValidationError("Rating must be in increments of 0.5.")
        return rating

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} ({self.rating})"
