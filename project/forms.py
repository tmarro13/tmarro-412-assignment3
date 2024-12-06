from django import forms
from .models import Movie, Review, Tag

# Form for searching movies using a text input field
class TMDbSearchForm(forms.Form):
    search_query = forms.CharField(
        label="Search for a movie",  # Label for the form field
        widget=forms.TextInput(attrs={  # HTML attributes for styling the input
            'placeholder': 'Enter movie title'  # Placeholder text in the input box
        }),
    )

# Form for associating tags with movies
class MovieForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),  # Fetch all available tags
        required=False,  # Tag selection is optional
        widget=forms.SelectMultiple(attrs={  # HTML widget for selecting multiple tags
            'class': 'tag-select',  # Custom class for styling
            'style': 'width: 100%;',  # Inline style for full-width dropdown
        }),
    )

    class Meta:
        model = Movie  # Associate the form with the Movie model
        fields = ['tags']  # Include only the 'tags' field in the form

# Form for creating or editing reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Associate the form with the Review model
        fields = ['rating', 'review_text']  # Include 'rating' and 'review_text' fields in the form
        widgets = {
            'rating': forms.NumberInput(attrs={  # HTML number input for rating
                'min': 1,  # Minimum value for rating
                'max': 10,  # Maximum value for rating
                'placeholder': 'Rate 1-10'  # Placeholder text
            }),
            'review_text': forms.Textarea(attrs={  # HTML textarea for the review text
                'placeholder': 'Write your review here...',  # Placeholder text
                'rows': 3  # Number of rows in the textarea
            }),
        }
        labels = {
            'rating': 'Rating (1-10)',  # Custom label for the 'rating' field
            'review_text': 'Review Text',  # Custom label for the 'review_text' field
        }
