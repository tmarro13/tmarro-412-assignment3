from django.core.management.base import BaseCommand
from project.views import add_movies_from_api

# Populates movies from the TMDB api.
class Command(BaseCommand):
    help = 'Populate the database with all movies from TMDB'

    def handle(self, *args, **kwargs):
        add_movies_from_api()
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with movies from TMDB without duplicates.'))
