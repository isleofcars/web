from django.urls import re_path as url
from django.urls import path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    url('', include('app.urls'))
]
urlpatterns += staticfiles_urlpatterns()
