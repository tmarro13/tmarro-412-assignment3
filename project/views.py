from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Tag
from .forms import MovieForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    success_url = reverse_lazy('movie_list')  # Use the name of your desired URL pattern

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'project/movie_list.html', {'movies': movies})

def movie_detail(request, pk):  # Changed 'movie_id' to 'pk'
    movie = get_object_or_404(Movie, id=pk)
    reviews = movie.reviews.all()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=movie.id)
    else:
        review_form = ReviewForm()

    return render(request, 'project/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
    })

@login_required
def add_movie(request):
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        new_tags = request.POST.get('new_tags', '').split(',')
        if movie_form.is_valid() and review_form.is_valid():
            # Save the movie
            movie = movie_form.save()
            # Save the review
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user  # Set the logged-in user as the reviewer
            review.save()
            # Handle new tags
            for tag_name in new_tags:
                tag_name = tag_name.strip()
                if tag_name:  # Avoid empty tags
                    tag, created = Tag.objects.get_or_create(name__iexact=tag_name, defaults={'name': tag_name})
                    movie.tags.add(tag)
            return redirect('movie_list')  # Redirect to the movie list page after adding
    else:
        movie_form = MovieForm()
        review_form = ReviewForm()
    return render(request, 'project/add_movie.html', {
        'movie_form': movie_form,
        'review_form': review_form
    })

@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'project/edit_movie.html', {'form': form, 'movie': movie})
