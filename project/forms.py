from django import forms
from .models import Movie, Review, Tag

class TMDbSearchForm(forms.Form):
    search_query = forms.CharField(
        label="Search for a movie",
        widget=forms.TextInput(attrs={'placeholder': 'Enter movie title'}),
    )

class MovieForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'tag-select',
            'style': 'width: 100%;',
        }),
    )

    class Meta:
        model = Movie
        fields = ['tags']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'placeholder': 'Rate 1-10'}),
            'review_text': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 3}),
        }
        labels = {
            'rating': 'Rating (1-10)',
            'review_text': 'Review Text',
        }
