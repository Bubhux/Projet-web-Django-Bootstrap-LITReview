from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from .validators import ContainsLetterValidator, ContainsNumberValidator


class LoginForm(forms.Form):
    """
    Formulaire de connexion.
    Ce formulaire est utilisé pour la saisie des informations de connexion.
    Il contient les champs 'username' (nom d'utilisateur) et 'password' (mot de passe).
    Attributes:
        username (CharField): Champ de saisie pour le nom d'utilisateur.
        password (CharField): Champ de saisie pour le mot de passe.
    """
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignUpForm(forms.ModelForm):
    """
    Formulaire d'inscription.
    Ce formulaire est utilisé pour l'inscription d'un nouvel utilisateur.
    Il hérite du modèle d'utilisateur spécifié dans la configuration.
    Il contient les champs 'username' (nom d'utilisateur), 'password' (mot de passe)
    et 'confirm_password' (confirmation du mot de passe).
    Attributes:
        password (CharField): Champ de saisie pour le mot de passe.
        confirm_password (CharField): Champ de saisie pour la confirmation du mot de passe.

    """
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
        """
        Validation du champ de mot de passe.
        Cette méthode effectue la validation personnalisée sur le champ de mot de passe.
        Elle vérifie la longueur minimale du mot de passe
        et la correspondance avec le champ de confirmation du mot de passe.
        Returns:
            str: Le mot de passe valide.
        Raises:
            ValidationError: Si la longueur minimale du mot de passe n'est pas respectée.
            ValidationError: Si les mots de passe ne correspondent pas.

        """
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
