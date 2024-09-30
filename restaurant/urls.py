from django.urls import path
from . import views  # Import views from the current app

# Define URL patterns
urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),  # URL for the main page
    path('order/', views.order, name='order'),  # URL for the order page
    path('confirmation/', views.confirmation, name='confirmation'),  # URL for the confirmation page
]
