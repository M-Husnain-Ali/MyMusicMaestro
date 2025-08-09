from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MusicManagerUser, Album, Song, AlbumTracklistItem

class UserRegistrationForm(UserCreationForm):
    """Form for registering new artist users"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    
    display_name = forms.CharField(
        max_length=512,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your artist name'
        }),
        help_text='Your artist name that will be displayed publicly and used to identify your albums'
    )
    
    class Meta:
        model = MusicManagerUser
        fields = ('username', 'email', 'display_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.display_name = self.cleaned_data['display_name']
        user.role = 'artist'  # Always set role to artist
        if commit:
            user.save()
        return user

class AlbumForm(forms.ModelForm):
    """
    A form for creating and updating Album instances. Tracklist is handled
    separately with a formset.
    """
    class Meta:
        model = Album
        fields = [
            'title', 'description', 'artist', 'price', 
            'format', 'release_date', 'cover_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AlbumTracklistItemForm(forms.ModelForm):
    """
    A form for an individual track in an album's tracklist.
    Used within a formset. The position is handled by drag-and-drop in the UI.
    """
    class Meta:
        model = AlbumTracklistItem
        fields = ['song', 'position']
        widgets = {
            'song': forms.Select(attrs={'class': 'form-control song-select'}),
            'position': forms.HiddenInput(),
        } 