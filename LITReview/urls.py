"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from authentication.views import SignUpPage, logout_user
from service.views import (
    home,
    flux,
    create_ticket,
    create_review,
    create_ticket_and_review,
    edit_ticket,
    edit_review,
    user_profile,
    update_profile_photo,
    followers_page
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Application authentication
    path('', LoginView.as_view(template_name='authentication/login.html',
                               redirect_authenticated_user=True), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpPage.as_view(), name='signup'),

    # Application service
    path('home/', home, name='home'),
    path('flux/', flux, name='flux'),
    path('create-ticket/', create_ticket, name='create_ticket'),
    path('create-review/', create_ticket_and_review, name='create_ticket_and_review'),
    path('create-review/<int:ticket_id>/', create_review, name='create_review'),

    path('edit-ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('edit-review/<int:review_id>/', edit_review, name='edit_review'),

    path('profile/<str:user>/', user_profile, name="user_profile"),
    path('update-profile-photo/', update_profile_photo, name="update_profile_photo"),
    path('profile/<str:user>/followers', followers_page, name="followers_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
