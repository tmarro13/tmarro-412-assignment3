from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# A model representing a Tag, which can be associated with multiple movies
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Name of the tag, must be unique

    def __str__(self):
        return self.name  # String representation of the tag, returns its name

# A model representing a Movie
class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True, null=True, blank=True)  # TMDb ID (optional, unique)
    title = models.CharField(max_length=200)  # Movie title
    director = models.CharField(max_length=200, blank=True, null=True)  # Director's name (optional)
    release_year = models.PositiveIntegerField(blank=True, null=True)  # Release year (optional)
    image = models.URLField(blank=True, null=True)  # URL for the movie's poster/image (optional)
    tags = models.ManyToManyField(Tag, related_name="tagged_movies", blank=True)  # Tags associated with the movie (optional)

    def __str__(self):
        return self.title  # String representation of the movie, returns its title

# A model representing a Review for a movie
class Review(models.Model):
    movie = models.ForeignKey(
        'Movie', 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )  # Foreign key to Movie, deletes reviews if the movie is deleted
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )  # Foreign key to User, deletes reviews if the user is deleted
    rating = models.PositiveIntegerField()  # Rating given to the movie
    review_text = models.TextField()  # Text of the review
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the review was created

    def clean_rating(self):
        # Validates that the rating is in increments of 0.5
        rating = self.cleaned_data.get('rating')  # Access the rating value from cleaned_data
        if rating % 0.5 != 0:  # Check if rating is not divisible by 0.5
            raise ValidationError("Rating must be in increments of 0.5.")  # Raise an error if invalid
        return rating  # Return the validated rating

    def __str__(self):
        # String representation of the review, includes movie title, user, and rating
        return f"{self.movie.title} - {self.user.username} ({self.rating})"
