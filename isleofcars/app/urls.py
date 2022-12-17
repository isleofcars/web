from django.urls import path

from app import views
# from views import account, login_view, register_view, logout_view, new_ad, \
#     settings, favorite, add_to_favorite, remove_from_favorite, \
#     ad_page

urlpatterns = [
    path('', views.render_homepage, name='ads'),
    path('ad/<int:ad_id>/', views.render_ad, name='ad_page'),
    # path('profile', views.render_profile, name='profile'),
    path('new-ad/', views.render_new_ad_form, name='new-ad'),
    path('favorites/', views.render_favorites, name='favorites'),
    path('profile-settings/', views.render_profile_settings, name='profile-settings'),
    # path('profile/favorite/add/<int:ad_id>', add_to_favorite, name='add_to_favorite'),
    # path('profile/favorite/remove/<int:ad_id>', remove_from_favorite, name='remove_from_favorite'),
    path('login/', views.login_view, name='login'),
    # path('register/', register_view, name='register'),
    # path('logout/', logout_view, name='logout'),
    path('like/', views.like, name='like'),

]
