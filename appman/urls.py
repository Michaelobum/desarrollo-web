from django.conf.urls import url
from django.contrib import admin
from appman.view_mediopago import viewmediopago
from django.urls import path
from appman.view_producto import viewproducto
from appman.view_marca import viewmarca
from seguridad.menu import menuinicial
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', menuinicial, name='inicio'),
    url(r'Producto/', viewproducto, name='producto'),
    url(r'Marca/', viewmarca, name='marca'),
    url(r'mediopago/', viewmediopago, name='mediopago'),]