from django.contrib import admin
from authentication.models import User
from django.contrib.contenttypes.models import ContentType
from service.models import Ticket, Review, UserFollows
from django.db import models


class TicketAdmin(admin.ModelAdmin):
    """
    Administration des tickets.
    Cette classe définit l'interface d'administration pour le modèle Ticket.
    Elle spécifie les champs à afficher dans la liste des tickets.
    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des tickets.
    """
    list_display = ('user', 'title')


class ReviewAdmin(admin.ModelAdmin):
    """
    Administration des critiques.
    Cette classe définit l'interface d'administration pour le modèle Review.
    Elle spécifie les champs à afficher dans la liste des critiques.
    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des critiques.
    """
    list_display = ('user', 'headline')


class UserFollowsAdmin(admin.ModelAdmin):
    """
    Administration des abonnements d'utilisateurs.
    Cette classe définit l'interface d'administration pour le modèle UserFollows.
    Elle spécifie les champs à afficher dans la liste des abonnements d'utilisateurs.
    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des abonnements d'utilisateurs.
    """
    list_display = ('user',)


class UserAdmin(admin.ModelAdmin):
    """
    Administration des utilisateurs.
    Cette classe définit l'interface d'administration pour le modèle User.
    Elle personnalisera l'affichage de la liste des utilisateurs en ajoutant des colonnes personnalisées.
    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des utilisateurs.
    """

    def get_follows_count(self, obj):
        """
        Obtient le nombre d'utilisateurs suivis par un utilisateur donné.
        Args:
            obj (User): L'instance de l'utilisateur.
        Returns:
            int: Le nombre d'utilisateurs suivis par l'utilisateur.
        """
        return obj.follows.count()

    get_follows_count.short_description = "Nombre d'utilisateurs suivis"
    
    def username_column(self, obj):
        """
        Renvoie le nom d'utilisateur d'un utilisateur donné.
        """
        return obj.username
    username_column.short_description = "Nom d'utilisateur"
    
    def follows_count_column(self, obj):
        """
        Renvoie le nombre d'utilisateurs suivis par un utilisateur donné.
        """
        return obj.follows.count()
    follows_count_column.short_description = "Nombre d'utilisateurs suivis"
    
    list_display = ('username_column', 'follows_count_column')

admin.site.register(User, UserAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
