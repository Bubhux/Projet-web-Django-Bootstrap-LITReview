from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from PIL import Image
from authentication.models import User


class Ticket(models.Model):
    """Class modéle pour les objests Ticket"""
    title = models.CharField(max_length=128, verbose_name='')
    description = models.TextField(max_length=2048, blank=True, verbose_name='')
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    has_review = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

    IMAGE_MAX_SIZE = (800, 800)

    def get_review_response(self):
        """Récupére la première critique associée au ticket"""
        review = self.review_set.first()
        if review:
            return review.response
        return None

    def resize_image(self):
        if self.image:
            image = Image.open(self.image.path)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    """Class modèle pour les objest Review"""
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='')
    headline = models.CharField(max_length=128, verbose_name='')
    body = models.TextField(max_length=2048, blank=True, verbose_name='')
    time_created = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class UserFollows(models.Model):
    """
    Classe du modèle UserFollows.
    L'utilisateur devra entrer un nom d'utilisateur.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        """
        S'assure que nous n'obtenons pas plusieurs instances
        de UserFollows pour une paire unique d'utilisateur-utilisateur_suivi (user-user_followed).
        """
        unique_together = ('user', 'followed_user')
