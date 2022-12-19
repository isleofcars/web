import operator
from functools import reduce

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from app import forms
from app.forms import RegisterForm, NewAddForm
from app.models import Favorite, CarAdvertisement


def render_homepage(request: HttpRequest) -> HttpResponse:
    """Render a main page with ads search."""
    ads = CarAdvertisement.objects.all()
    for key, values in request.GET.lists():
        if key in {'search', 'page'} or values == ['']:
            continue
        ads = ads.filter(Q(**{f'{key}__in': values}))
    search = request.GET.get('search')
    if search:
        search = search.split()
        # TODO: Search in make/model/description/etc
        tag_qs = reduce(operator.and_, (Q(title__icontains=x) for x in search))
        ads = ads.filter(tag_qs)
    favorites = request.user.favorite_set.values_list('ads_id', flat=True)
    for ad in ads:
        ad.is_favorite = ad.id in favorites
    paginator = Paginator(ads, per_page=25)
    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)
    return render(
        request=request,
        template_name='home.html',
        context=dict(
            ads=ads,
            filters_form=forms.FiltersForm(request.GET)
        )
    )


def render_new_ad_form(request: HttpRequest) -> HttpResponse:
    """Render a page to add a new advertisement."""
    return render(
        request=request,
        template_name='new_ad.html',
        context=dict(
            form=NewAddForm()
        )
    )


def save_new_ad(request: HttpRequest) -> HttpResponse:
    """Save a new advertisement."""
    if request.method == 'POST':
        # new = CarAdvertisement()
        form = NewAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # form = NewAddForm()
    # return render(
    #     request=request,
    #     template_name='new_ad.html',
    #     context=dict(
    #         form=NewAddForm()
    #     )
    # )


# TODO: Add check login decorator
def render_profile_settings(request: HttpRequest) -> HttpResponse:
    """Render a user profile settings page."""
    return render(
        request=request,
        template_name='profile-settings.html',
        context={}
    )


def render_ad(request: HttpRequest, ad_id: int) -> HttpResponse:
    """Render an advertisement page."""
    ctx = {}
    ad = CarAdvertisement.objects.get(id=ad_id)
    ad = model_to_dict(ad)
    ctx["title"] = ad["title"]
    ctx["id"] = ad["id"]
    ctx["ad"] = ad
    return render(request, 'ad_page.html', ctx)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('ads')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form":form})


def register_view(request):
    if request.method == 'GET':
        form  = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            user = authenticate(username=user, password=pw)
            if user is not None:
                login(request, user)
            messages.success(request, 'Account was created for ' + str(user))
            return redirect('profile')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'register.html', context)

    return render(request, 'register.html', {})


def logout_view(request):
    logout(request)
    return redirect('ads')




def settings(request):
    """In settings avalible only password change"""

    ctx = {}
    if str(request.user) == 'AnonymousUser':
        ctx["auth"] = False
    else:
        ctx["auth"] = True
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            ctx["form"] = PasswordChangeForm(request.user)
    return render(request, 'settings.html', ctx)



# TODO: Add check login decorator
def render_favorites(request: HttpRequest) -> HttpResponse:
    """Render favorite ads of a user."""
    # TODO: Consider how to show sold items here.
    ads = Favorite.objects.get(user_id=request.user).ads_id.all()
    for ad in ads:
        ad.is_favorite = True
    paginator = Paginator(ads, per_page=25)
    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)
    return render(
        request=request,
        template_name='favorites.html',
        context=dict(
            ads=ads
        )
    )


# TODO: Check if POST
# TODO: Check if ajax
# TODO: Check if user logged in
def like(request: HttpRequest) -> JsonResponse:
    ad_id = request.POST['ad_id']
    print('like', ad_id)
    ad = CarAdvertisement.objects.get(id=ad_id)
    try:
        favorite = Favorite.objects.get(user_id=request.user)
    except Favorite.DoesNotExist:
        favorite = Favorite.objects.create(user_id=request.user)
    favorite.ads_id.add(ad)
    print('success!')
    return JsonResponse({})


# TODO: Check if POST
# TODO: Check if ajax
# TODO: Check if user logged in
def unlike(request: HttpRequest) -> JsonResponse:
    ad_id = request.POST['ad_id']
    print('unlike', ad_id)
    ad = CarAdvertisement.objects.get(id=ad_id)
    try:
        favorite = Favorite.objects.get(user_id=request.user)
    except Favorite.DoesNotExist:
        favorite = Favorite.objects.create(user_id=request.user)
    favorite.ads_id.remove(ad)
    print('success!')
    return JsonResponse({})
