from django.urls import path
from django.contrib.auth import views as auth_views

from .views import account, login_view, register_view, logout_view, new_ad, ads_list, settings, favorite, add_to_favorite, remove_from_favorite, ad_page
urlpatterns = [
    path('', ads_list, name='ads'),
    path('<int:page>', ads_list, name='ads_by_page'),
    path('cars/<int:ad_id>', ad_page, name='ad_page'),
    path('profile/', account, name='profile'),
    path('profile/settings/', settings, name='settings'),
    path('profile/favorite/', favorite, name='favorite'),
    path('profile/favorite/add/<int:ad_id>', add_to_favorite, name='add_to_favorite'),
    path('profile/favorite/remove/<int:ad_id>', remove_from_favorite, name='remove_from_favorite'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('new_ad/', new_ad, name='new_ad'),
]
