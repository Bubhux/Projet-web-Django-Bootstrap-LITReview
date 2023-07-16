from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):
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


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    if instance.pk is None:
        # Effectuer les opérations personnalisées pour un nouvel utilisateur
        instance.password = make_password(instance.password)

