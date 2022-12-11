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

from .forms import RegisterForm, NewAddForm
from .models import Favorite
from app.models import CarAdvertisement


def ads_list(request, page=1):
    ctx = {}
    ads = CarAdvertisement.objects.all().order_by("id").reverse()
    paginator = Paginator(ads, per_page=20)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)
    ctx["page_obj"] = page_object
    for obj in page_object:
        if len(obj.photos) == 0:
            obj.photos.append("https://www.rehab.cv.ua/wp-content/themes/apexclinic/images/no-image/No-Image-Found-400x264.png")
        elif type(obj.photos[0]) != str:
            obj.photos[0] = "https://www.rehab.cv.ua/wp-content/themes/apexclinic/images/no-image/No-Image-Found-400x264.png"
        elif len(obj.photos[0]) <= 7:
            obj.photos[0] = "https://www.rehab.cv.ua/wp-content/themes/apexclinic/images/no-image/No-Image-Found-400x264.png"
    return render(request, "ads.html", context=ctx)


def account(request):
    ctx = {}
    if str(request.user) == 'AnonymousUser':
        ctx["auth"] = False
    else:
        ctx["auth"] = True
    return render(request, 'profile.html', ctx)


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
                return redirect("profile")
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

def new_ad(request):
    if request.method == 'POST':
        new = CarAdvertisement()
        form = NewAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ads')
    form = NewAddForm()
    ctx = {
        "form": form
    }
    return render(request, 'new_ad.html', ctx)


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


def favorite(request):
    ctx = {}
    if str(request.user) == 'AnonymousUser':
        ctx["auth"] = False
    else:
        ctx["auth"] = True
        try:
            fav = Favorite.objects.get(user_id=request.user.id)
        except Favorite.DoesNotExist:
            user = User.objects.get(id=request.user.id)
            fav = Favorite.objects.create(user_id=user)
        ctx["fav"] = fav.ads_id.all()

    return render(request, 'favorite.html', ctx)


def add_to_favorite(request, ad_id):
    ctx = {}
    if str(request.user) == 'AnonymousUser':
        pass #Add message
    else:
        user = User.objects.get(id=request.user.id)
        try:
            ad = CarAdvertisement.objects.get(id=ad_id)
            favorite = Favorite.objects.get(user_id=user)
        except Favorite.DoesNotExist:
            ad = CarAdvertisement.objects.get(id=ad_id)
            favorite = Favorite.objects.create(user_id=user)
        favorite.ads_id.add(ad)
    return redirect('favorite')


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


def ad_page(request, ad_id):
    ctx = {}
    ad = CarAdvertisement.objects.get(id=ad_id)
    ad = model_to_dict(ad)
    ctx["title"] = ad["title"]
    ctx["id"] = ad["id"]
    ctx["ad"] = ad
    return render(request, 'ad_page.html', ctx)