from django import forms
from .models import Profile
from .models import StatusMessage


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'city', 'email', 'image_url']
        widgets = {
            'firstname': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Profile Image URL'}),
        }
        labels = {
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'city': 'City',
            'email': 'Email Address',
            'image_url': 'Profile Image URL',
        }

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'Status message',
                'rows': 3,
                'cols': 40,
                'class': 'status-textarea',
            }),
        }
        labels = {
            'message': 'Your Status',
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email']

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']