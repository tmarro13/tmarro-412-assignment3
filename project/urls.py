from django.urls import path, include
from django.contrib import admin
from . import views
from .views import signup, CustomLoginView

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('add/', views.add_movie, name='add_movie'),  # Add movie page
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path("accounts/signup/", signup, name="signup"),
]
