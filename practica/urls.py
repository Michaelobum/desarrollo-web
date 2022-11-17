from django.conf.urls import url
from django.contrib import admin
from appman.view_mediopago import viewmediopago
from django.urls import path
from django.urls.conf import include
from appman import urls
from appman.view_producto import viewproducto
from appman.view_marca import viewmarca
from seguridad.menu import menuinicial
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'', include('appman.urls'))
]
