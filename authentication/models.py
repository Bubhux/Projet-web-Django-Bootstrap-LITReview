from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class User(AbstractUser):
    """
    Modèle personnalisé d'utilisateur.
    Ce modèle étend le modèle d'utilisateur de base djangos.contrib.auth.models.AbstractUser.
    Il ajoute des champs supplémentaires pour gérer les abonnements et les photos de profil des utilisateurs.
    """
    password = models.CharField(max_length=128, validators=[])
    profile_photo = models.ImageField(blank=True, null=True, verbose_name='photo de profil ')
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit'
    )
    followed_by_user = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following_users',
        blank=True,
        verbose_name='suivi par'
    )


@receiver(pre_save, sender=get_user_model())
def user_pre_save(sender, instance, **kwargs):
    """
    Ce décorateur est utilisé pour associer la fonction `user_pre_save` au signal `pre_save` du modèle User.
    Le signal `pre_save` est déclenché avant l'enregistrement d'une instance du modèle User.
    Fonction de rappel pré-enregistrement pour le modèle User.
    Cette fonction est déclenchée avant l'enregistrement d'un utilisateur.
    Si l'utilisateur est nouveau (pk=None), elle effectue des opérations personnalisées sur le mot de passe,
    en utilisant la fonction make_password() pour le hacher avant de l'enregistrer dans la base de données.
    Args:
        sender (Model): Le modèle qui envoie le signal.
        instance (User): L'instance de l'utilisateur en cours d'enregistrement.
        **kwargs: Des arguments supplémentaires.

    """
    if instance.pk is None:
        # Effectuer les opérations personnalisées pour un nouvel utilisateur
        instance.password = make_password(instance.password)
