from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse

from app.forms import RegisterForm, NewAddForm
from app.models import Favorite, CarAdvertisement


def render_homepage(request: HttpRequest) -> HttpResponse:
    """Render a main page with ads search."""
    # TODO: Implement infinite scroll
    # TODO: Add Masonry view
    ads = CarAdvertisement.objects.all()
    favorites = request.user.favorite_set.values_list('ads_id', flat=True)
    print('favorites', favorites)
    for ad in ads:
        ad.is_favorite = ad.id in favorites
    paginator = Paginator(ads, per_page=25)
    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)
    # ctx = {}
    # page_object = paginator.get_page(page)
    # page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)
    # ctx["page_obj"] = page_object
    # for obj in page_object:
    #     if len(obj.photos) == 0:
    #         obj.photos.append("https://www.rehab.cv.ua/wp-content/themes/apexclinic/images/no-image/No-Image-Found-400x264.png")
    #     elif type(obj.photos[0]) != str:
    #         obj.photos[0] = "https://www.rehab.cv.ua/wp-content/themes/apexclinic/images/no-image/No-Image-Found-400x264.png"
    #     elif len(obj.photos[0]) <= 7:
    #         obj.photos[0] = "https://www.rehab.cv.ua/wp-content/themes/apexclinic/images/no-image/No-Image-Found-400x264.png"
    return render(
        request=request,
        template_name='home.html',
        context=dict(ads=ads)
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
def render_favorites(request: HttpRequest) -> HttpResponse:
    """Render favorite ads of a user."""
    # TODO: Consider how to show sold items here.
    ads = Favorite.objects.filter(user_id=request.user.id)
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


# TODO: Check if POST
# TODO: Check if user logged in
def like(request: HttpRequest) -> JsonResponse:
    ad_id = request.POST['ad_id']
    print('like', ad_id)
    Favorite.objects.get_or_create(user_id=request.user.id).add(
        CarAdvertisement.objects.get(id=ad_id)
    )
    print('success!')
    return JsonResponse({})


def remove_from_favorite(request, ad_id):
    if str(request.user) == 'AnonymousUser':
        pass #Add message
    else:
        user = User.objects.get(id=request.user.id)
        try:
            ad = CarAdvertisement.objects.get(id=ad_id)
            favorite = Favorite.objects.get(user_id=user)
        except Favorite.DoesNotExist:
            return redirect('favorite')
        favorite.ads_id.remove(ad)
    return redirect('favorite')
