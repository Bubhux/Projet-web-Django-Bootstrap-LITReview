from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from PIL import Image
from authentication.models import User


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name='Titre')
    description = models.TextField(max_length=2048, blank=True, verbose_name='Description')
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    has_review = models.BooleanField(default=False)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        verbose_name='Note'
    )

    headline = models.CharField(max_length=128, verbose_name='Titre')
    body = models.TextField(max_length=8192, blank=True, verbose_name='Critique')
    time_created = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class UserFollows(models.Model):
    """
    Class of the UserFollows model.
    The user will need to enter a user name
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        """
        Ensures we don't get multiple UserFollows instances
        for unique user-user_followed pairs
        """
        unique_together = ('user', 'followed_user')
