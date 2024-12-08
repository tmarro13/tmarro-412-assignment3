from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Tag
from .forms import ReviewForm
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

TMDB_API_KEY = "4e1f24cce8b996495e799b1b44d89e84"

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            from django.contrib.auth import login
            login(request, user)
            return redirect('movie_list')  # Redirect to the movie list page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def tmdb_search(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": query,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
    return render(request, 'tmdb_search.html', {'query': query, 'results': results})

# Home or movie list view
def movie_list(request):
    query = request.GET.get("query", "")
    tag_id = request.GET.get("tag", "")
    

    # Annotate movies with review count
    movies = Movie.objects.annotate(review_count=Count('reviews'))
    
    # Filter by query (search term)
    if query:
        movies = movies.filter(title__icontains=query)
    
    # Filter by tag if a tag ID is provided
    if tag_id:
        movies = movies.filter(tags__id=tag_id)
    
    # Order by the number of reviews in descending order
    movies = movies.order_by('-review_count')
    
    paginator = Paginator(movies, 50)  # Show 50 movies per page (can be adjusted)
    page = request.GET.get('page')

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    page_obj = movies
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages

    pagination_range = [
        n for n in range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))
    ]
    
    # Fetch all tags for the dropdown
    tags = Tag.objects.all()

    return render(request, "project/movie_list.html", {"movies": movies, "page_obj": page_obj, "pagination_range": pagination_range, "tags": tags, "selected_tag": tag_id, "query": query})

def highest_rated_movies(request):
    tag_id = request.GET.get("tag", "")
    query = request.GET.get("query", "")  # Get search term

    movies = Movie.objects.annotate(average_rating=Avg('reviews__rating'))

    # Filter by query (search term)
    if query:
        movies = movies.filter(title__icontains=query)
    
    # Filter by tag if a tag ID is provided
    if tag_id:
        movies = movies.filter(tags__id=tag_id)

    # Order by the number of reviews in descending order
    movies = movies.order_by('-average_rating')

    paginator = Paginator(movies, 50)  # Show 50 movies per page
    page = request.GET.get('page')

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    page_obj = movies
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages

    pagination_range = [
        n for n in range(max(1, current_page - 2), min(total_pages + 1, current_page + 3))
    ]

    # Fetch all tags for filtering
    tags = Tag.objects.all()  # Ensure tags are fetched for the dropdown

    return render(request, 'project/highest_rated_movies.html', {'movies': movies, 'page_obj': page_obj, "pagination_range": pagination_range, 'tags': tags, 'selected_tag': tag_id, 'query': query})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)  # Ensure only the owner can delete
    if request.method == "POST":
        review.delete()
        return redirect('my_reviews')  # Redirect to "My Reviews" after deletion
    return HttpResponseForbidden("Invalid request method.")  # Disallow non-POST requests

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'project/my_reviews.html', {'reviews': reviews})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)  # Ensure the user can only edit their reviews
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('my_reviews')  # Redirect to the "My Reviews" page after saving
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'project/edit_review.html', {'form': form, 'review': review})

# Movie detail view
def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.annotate(average_rating=Avg('reviews__rating')), id=pk)
    reviews = Review.objects.filter(movie=movie)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to post a review.")
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=movie.id)
    else:
        review_form = ReviewForm()

    
    context = {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
        'average_rating': movie.average_rating,
    }
    return render(request, 'project/movie_detail.html', context)


# Search for movies using TMDb API
def fetch_director(movie_id, api_key):
    """Fetch the director of a movie from TMDB."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        credits_data = response.json()
        crew = credits_data.get("crew", [])
        for member in crew:
            if member.get("job") == "Director":
                return member.get("name")
    return "Unknown"

import requests
from project.models import Movie, Tag

def add_movies_from_api():
    api_key = "4e1f24cce8b996495e799b1b44d89e84"
    base_url = "https://api.themoviedb.org/3/movie/popular"
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
    page = 1  # Start with the first page

    # Fetch all genres and create Tag entries if they don't already exist
    genre_response = requests.get(genre_url)
    if genre_response.status_code != 200:
        print(f"Failed to fetch genres from TMDB: {genre_response.status_code}")
        return

    genres_data = genre_response.json().get("genres", [])
    genre_map = {}  # Map genre IDs to Tag objects

    for genre in genres_data:
        tag, created = Tag.objects.get_or_create(name=genre["name"])
        genre_map[genre["id"]] = tag

    while True:
        # Fetch movies page by page
        url = f"{base_url}?api_key={api_key}&language=en-US&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch movies from TMDB: {response.status_code}")
            break

        data = response.json()
        results = data.get("results", [])

        # If no more results, stop pagination
        if not results:
            break

        for movie_data in results:
            title = movie_data.get("title")
            release_year = movie_data.get("release_date", "").split("-")[0] if movie_data.get("release_date") else None
            image_url = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}" if movie_data.get("poster_path") else None
            genre_ids = movie_data.get("genre_ids", [])

            # Check if the movie already exists in the database
            if not Movie.objects.filter(title=title, release_year=release_year).exists():
                # Fetch the director
                movie_id = movie_data.get("id")
                director = fetch_director(movie_id, api_key)

                # Create the movie entry
                movie = Movie.objects.create(
                    title=title,
                    director=director,
                    release_year=release_year,
                    image=image_url,
                )

                # Add tags (genres) to the movie
                for genre_id in genre_ids:
                    tag = genre_map.get(genre_id)
                    if tag:
                        movie.tags.add(tag)

        # Increment the page number to fetch the next page
        page += 1

        # Stop if there are no more pages
        if page > data.get("total_pages", 1):
            break

def populate_movies(request):
    add_movies_from_api()
    messages.success(request, 'Movies successfully populated from TMDB.')
    return redirect('movie_list')

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')  # Sort reviews by most recent
    return render(request, 'project/review_list.html', {'reviews': reviews})