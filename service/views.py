from itertools import chain
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from service.models import Ticket, Review
from authentication.models import User
from django.contrib import messages
from service.models import Response
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.urls import reverse


from .forms import FollowUserButton, UnfollowUserButton, ReviewForm
from . import forms, models


@login_required
def home(request):
    user = request.user
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    user_follows = user.follows.all()
    user_followers = user.followed_by_user.all()

    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)

    paginator = Paginator(tickets_and_reviews, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'service/home.html', context={
        'page_obj': page_obj,
        'tickets': tickets,
        'reviews': reviews,
        'requested_user': request.user,
        'user': user,
        'user_follows': user_follows,
        'user_followers': user_followers}
    )


@login_required
def flux(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()

    hide_reviews = request.GET.get('hide_reviews') == 'on'
    hide_tickets = request.GET.get('hide_tickets') == 'on'
    hide_reviewed_tickets = request.GET.get('hide_reviewed_tickets') == 'on'

    filtered_tickets = tickets
    filtered_reviews = reviews

    if hide_tickets:
        filtered_tickets = models.Ticket.objects.none()

    if hide_reviews:
        filtered_reviews = models.Review.objects.none()

    if hide_reviewed_tickets:
        filtered_tickets = filtered_tickets.exclude(has_review=True)

    tickets_and_reviews = sorted(chain(filtered_tickets, filtered_reviews), key=lambda instance: instance.time_created, reverse=True)

    paginator = Paginator(tickets_and_reviews, 4)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'service/flux.html', context={
        'page_obj': page_obj,
        'hide_reviews': hide_reviews,
        'hide_tickets': hide_tickets,
        'hide_reviewed_tickets': hide_reviewed_tickets
    })


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            if form.cleaned_data['image']:
                ticket.image = form.cleaned_data['image']

            ticket.has_review = False
            ticket.save()
            return redirect('home')

    return render(request, 'service/create_ticket.html', context={'form': form})


@login_required
def create_review(request, ticket_id=None):
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)

    reviews = models.Review.objects.filter(user=request.user)
    ticket_form = forms.TicketForm(request.POST or None, request.FILES or None)
    review_form = forms.ReviewForm(request.POST or None)

    if request.method == 'POST':
        if ticket_id:
            # Cas où un ticket existe
            if ticket:
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.ticket = ticket
                    review.save()
                    return redirect('flux')
            else:
                form = ReviewForm()
                # Cas où le ticket n'existe pas
                if ticket_form.is_valid() and review_form.is_valid():
                    ticket = ticket_form.save(commit=False)
                    ticket.user = request.user
                    if ticket_form.cleaned_data['image']:
                        ticket.image = ticket_form.cleaned_data['image']
                    ticket.has_review = True
                    ticket.save()

                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.ticket = ticket
                    review.rating = int(request.POST['rating'])
                    review.save()
                    return HttpResponseRedirect(reverse('flux'))

                if ticket.has_review and ticket.review_set.first().user != request.user:
                    return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette réponse.")

    context = {'ticket_form': ticket_form, 'review_form': review_form, 'ticket': ticket, 'ticket_id': ticket_id}
    return render(request, 'service/create_review.html', context=context)


@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if ticket_form.cleaned_data['image']:
                ticket.image = ticket_form.cleaned_data['image']

            ticket.has_review = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = get_object_or_404(models.Ticket, id=ticket.id)
            review.save()
            return redirect('flux')

    return render(request, 'service/create_review.html', context={'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.TicketFormDelete()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('flux')
        if 'delete_ticket' in request.POST:
            delete_form = forms.TicketFormDelete(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('flux')

    return render(request, 'service/edit_ticket.html', context={'edit_form': edit_form, 'delete_form': delete_form})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.ReviewFormDelete()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('flux')
        if 'delete_review' in request.POST:
            delete_form = forms.ReviewFormDelete(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('flux')

    return render(request, 'service/edit_review.html', context={'edit_form': edit_form, 'delete_form': delete_form})


@login_required
def user_profile(request, user):
    user = User.objects.get(username=user)
    user_follows = user.follows.all()
    user_followers = user.followed_by_user.all()
    tickets = Ticket.objects.filter(user=user.id)
    reviews = Review.objects.filter(user=user.id)

    follow_form = forms.FollowUserButton(initial={'user_to_follow': user.id})
    if request.user.follows.filter(id=user.id).exists():
        btn_text = "Se désabonner"
    else:
        btn_text = "S'abonner"

    if request.method == 'POST':
        follow_form = forms.FollowUserButton(request.POST)
        if follow_form.is_valid():
            user_to_follow = get_object_or_404(User, id=follow_form.cleaned_data['user_to_follow'])
            if request.user.follows.filter(id=user_to_follow.id).exists():
                request.user.follows.remove(user_to_follow)
                user_to_follow.followed_by_user.remove(request.user)
                btn_text = "S'abonner"
            else:
                request.user.follows.add(user_to_follow)
                user_to_follow.followed_by_user.add(request.user)
                btn_text = "Se désabonner"

    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)

    #print(requested_user.username)
    
    return render(request, 'service/user_profile.html', context={
        'follow_form': follow_form,
        'btn_text': btn_text,
        'requested_user': user,
        'user_follows': user_follows,
        'user_followers': user_followers,
        'tickets_and_reviews': tickets_and_reviews}
    )


@login_required
def update_profile_photo(request):
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile/' + request.user.username)
    else:
        form = forms.UploadProfilePhotoForm()

    return render(request, 'service/update_profile_photo.html', context={'form': form})


@login_required
def followers_page(request, user):
    search_form = forms.SearchUser()
    searched_user_resp = ""
    requested_user = User.objects.get(username=user)
    searched_user_resp_btn = ''

    user_follows = requested_user.follows.all()
    user_followers = requested_user.followed_by_user.all()

    group_user_follows = {}
    for user in user_follows:
        follow_form = forms.FollowUserButton(initial={'user_to_follow': user.id})
        group_user_follows[user] = follow_form

    # Créez le formulaire pour se désabonner
    unfollow_form = UnfollowUserButton()

    if request.method == 'POST':
        follow_form = forms.FollowUserButton(request.POST)
        unfollow_form = UnfollowUserButton(request.POST)
        if follow_form.is_valid():
            user_to_follow = get_object_or_404(User, id=follow_form.cleaned_data['user_to_follow'])
            if request.user.follows.filter(id=user_to_follow.id).exists():
                request.user.follows.remove(user_to_follow)
                user_to_follow.followed_by_user.remove(request.user)

            else:
                request.user.follows.add(user_to_follow)
                user_to_follow.followed_by_user.add(request.user)
                messages.success(request, "Abonnement effectué avec succès.")
            return redirect('followers_page', user=request.user.username)

        elif unfollow_form.is_valid():
            user_to_unfollow = get_object_or_404(User, id=unfollow_form.cleaned_data['user_to_unfollow'])
            request.user.follows.remove(user_to_unfollow)
            user_to_unfollow.followed_by_user.remove(request.user)
            messages.success(request, "Désabonnement effectué avec succès.")
            return redirect('followers_page', user=request.user.username)
    else:
        follow_form = forms.FollowUserButton()
        unfollow_form = UnfollowUserButton()

    search_form = forms.SearchUser(request.POST)
    if search_form.is_valid():
        query = search_form.cleaned_data['search']
        searched_user = User.objects.filter(username__icontains=query).first()
        if searched_user:
            searched_user_resp = searched_user
            searched_user_resp_btn = forms.FollowUserButton(initial={'user_to_follow': searched_user.id})

    return render(request, 'service/followers.html', context={
        'search_form': search_form,
        'searched_user_resp': searched_user_resp,
        'searched_user_btn': searched_user_resp_btn,
        'requested_user': requested_user,
        'user_follows': user_follows,
        'group_user_follows': group_user_follows,
        'follow_form': follow_form,
        'unfollow_form': unfollow_form,
        'user_followers': user_followers}
    )
