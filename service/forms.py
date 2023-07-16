from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from . import models

#User = get_user_model()


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg, image/png, image/gif'}),
        }


class TicketFormDelete(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'body', 'rating']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Critique'}),
            'rating': forms.RadioSelect(attrs={'class': 'custom-radio-class'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs['class'] = 'form-control'


class ReviewFormDelete(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['profile_photo']
        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={'accept': 'image/jpeg, image/png, image/gif', 'name': 'photo'}),
        }


class FollowUserButton(forms.Form):
    user_to_follow = forms.CharField(widget=forms.HiddenInput())


class UnfollowUserButton(forms.Form):
    user_to_unfollow = forms.IntegerField(widget=forms.HiddenInput())


class SearchUser(forms.Form):
    search = forms.CharField(
        label=False,
        widget=forms.TextInput(
        attrs={'placeholder': 'Rechercher un utilisateur'})
    )

    #search_user_id = forms.BooleanField(widget=forms.HiddenInput, initial=True)

