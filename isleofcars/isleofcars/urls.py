from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('app.urls'))
]
urlpatterns += staticfiles_urlpatterns()
print('staticfiles_urlpatterns', staticfiles_urlpatterns())
