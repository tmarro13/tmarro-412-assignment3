from django import forms
from .models import Movie, Review, Tag

class MovieForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'tag-select',
            'style': 'width: 100%;',  # Optional for styling
        }),
        help_text="Select existing tags.",
    )
    new_tags = forms.CharField(
        required=False,
        help_text="Enter new tags separated by commas.",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter new tags',
        }),
    )

    class Meta:
        model = Movie
        fields = ['title', 'director', 'release_year', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1, 
                'max': 10, 
                'step': 1, 
                'placeholder': 'Rate 1 to 10'
            }),
            'review_text': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Write your review here...'
            }),
        }
        labels = {
            'rating': 'Rating (1-10)',
            'review_text': 'Review Text',
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description', 'movies']