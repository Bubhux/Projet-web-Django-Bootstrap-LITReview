from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.contrib.auth.password_validation import validate_password

from .validators import ContainsLetterValidator, ContainsNumberValidator


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Mot de passe',
        help_text=format_html(
            '{}<br>{}',
            ContainsLetterValidator().get_help_text(),
            ContainsNumberValidator().get_help_text()
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmez le mot de passe'
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        # Vérifier la longueur minimale du mot de passe
        if len(password) < 8:
            raise ValidationError('Le mot de passe doit avoir au moins 8 caractères')

        # Vérifier la correspondance avec le champ de confirmation du mot de passe
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Les mots de passe ne correspondent pas")

        return password

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'confirm_password']
