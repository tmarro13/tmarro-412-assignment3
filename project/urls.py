from django.urls import path, include
from django.contrib import admin
from . import views
from .views import signup
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('search/', views.tmdb_search, name='tmdb_search'),
    path('reviews/', views.review_list, name='review_list'),
    path('highest-rated-movies/', views.highest_rated_movies, name='highest_rated_movies'),
    path('all-reviews/', views.review_list, name='review_list'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('edit-review/<int:pk>/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    
] 
