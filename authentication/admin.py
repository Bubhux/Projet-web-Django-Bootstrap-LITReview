from django.contrib import admin
from authentication.models import User
from django.contrib.contenttypes.models import ContentType
from service.models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):

    list_display = ('user', 'title')


class ReviewAdmin(admin.ModelAdmin):

    list_display = ('user', 'headline')


class UserFollowsAdmin(admin.ModelAdmin):

    list_display = ('user',)


class UserAdmin(admin.ModelAdmin):

    list_display = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)