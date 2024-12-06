from django.contrib import admin
from .models import Movie, Review, Tag

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'display_tags', 'release_year')  # Use display_tags for tags
    search_fields = ('title', 'director', 'tags__name')  # Search tags by name
    list_filter = ('tags', 'release_year')  # Use tags for filtering

    def display_tags(self, obj):
        """Show tags as a comma-separated list."""
        return ", ".join(tag.name for tag in obj.tags.all())
    
    display_tags.short_description = 'Tags'  # Label for the tags column

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at') 
    search_fields = ('movie__title', 'user__username')
    list_filter = ('rating', 'created_at')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
