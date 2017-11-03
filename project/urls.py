"""seriesDjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from seriesDjangoProject import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^welcome/', views.welcome),
    url(r'^signIn/', views.signIn),
    url(r'^search/', views.search),
    url(r'^logIn/', views.logIn),
    url(r'^logout/', views.logOut),
    url(r'^signIn/', views.signIn),
    url(r'^addToFavorites/(?P<id>[0-9]+)/$', views.addToFavorites),
    url(r'^removeFromFavorites/(?P<id>[0-9]+)/$', views.removeFromFavorites)
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
