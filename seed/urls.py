"""
URL configuration for seed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',movierulz),
    path('login/',signin),
    path('logout/',signout),
    path('files/',files),
    path('player/<int:id>',player),
    path('playfolder/<int:id>',playfolder),
    path('downloadfolderfile/<int:id>',downloadfolderfile),
    path('download/<int:id>',download),
    path('deletefolder/<str:id>',deletefolder),
    path('deletefile/<str:id>/<int:fid>',deletefile),
    path('open/<int:id>',openfolder),

    path('movie/',movie),
    path('watch/',watch),
    path('addtorrent/',addtorrent),
    path('tamilmv/',home),
    path('movierulz/movie/',movierulzmovie),
    path('youtube/',youtube),
    path('search/',mainsearch),
    path('solid/',solidtorrent),




]
