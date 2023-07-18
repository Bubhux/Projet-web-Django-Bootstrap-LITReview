from django import forms
from django.contrib.auth import get_user_model


from . import models


class TicketForm(forms.ModelForm):
    """Formulaire de ticket permettant de créer et de modifier un ticket."""
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    # Configuration du modèle Ticket et des champs à inclure dans le formulaire
    # Définition des widgets pour chaque champ, avec des attributs spécifiques
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg, image/png, image/gif'}),
        }


class TicketFormDelete(forms.Form):
    """Formulaire de suppression de critique."""
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    """Formulaire de critique permettant de créer et de modifier une critique."""
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    # Configuration du modèle Review et des champs à inclure dans le formulaire
    # Définition des widgets pour chaque champ, avec des attributs spécifiques
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
    """Formulaire de suppression de critique."""
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UploadProfilePhotoForm(forms.ModelForm):
    """Formulaire de téléchargement de photo de profil."""

    # Configuration du modèle utilisateur actif et du champ profile_photo à inclure dans le formulaire
    # Définition des widgets pour chaque champ, avec des attributs spécifiques
    class Meta:
        model = get_user_model()
        fields = ['profile_photo']
        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={
                'accept': 'image/jpeg, image/png, image/gif', 'name': 'photo'}),
        }


class FollowUserButton(forms.Form):
    """Formulaire de bouton pour suivre un utilisateur."""
    user_to_follow = forms.CharField(widget=forms.HiddenInput())


class UnfollowUserButton(forms.Form):
    """Formulaire de bouton pour ne plus suivre un utilisateur."""
    user_to_unfollow = forms.IntegerField(widget=forms.HiddenInput())


class SearchUser(forms.Form):
    """Formulaire de recherche d'utilisateur."""

    # Champ de recherche d'utilisateur avec un attribut placeholder
    search = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher un utilisateur'})
    )
