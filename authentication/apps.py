from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Classe de configuration pour le module d'authentification.
    Cette classe définit la configuration de l'application d'authentification.
    Elle hérite de la classe de base `AppConfig` de Django.
    Attributes:
        default_auto_field (str): Le nom du champ d'auto-incrémentation utilisé par défaut pour les modèles.
        name (str): Le nom de l'application.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
