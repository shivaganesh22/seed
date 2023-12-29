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
from django.urls import path,include
from app.views import *
from api import urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',signin),
    path('logout/',signout),

    path('',movierulz),
    path('movierulz/movie/',movierulzmovie),
    path('tamilmv/movie/',tamilmvmovie),
    path('tamilmv/',tamilmv),
    path('ibomma/movie/',ibommamovie),
    path('ibomma/',ibomma),
    path('doodplay/',doodplay),
    
    path('sports/',sports),
    path('sports/player/',sportsplayer),

    path('files/',folders),
    path('playfolder/<int:id>',playfolder),
    path('downloadfolderfile/<int:id>',downloadfolderfile),
    path('deletefolder/<str:id>',deletefolder),
    path('renamefolder/<int:id>/',renamefolder),

    path('open/<int:id>',openfolder),
    path('player/<int:id>',player),
    path('download/<int:id>',download),
    path('deletefile/<str:id>/<int:fid>',deletefile),
    path('renamefile/<int:fid>/<int:id>/',renamefile),
    path('renamefile/<int:id>/',renamefilehome),

    path('addtorrent/',addtorrent),
    path('deletetorrent/<int:id>',deletetorrent),

    path('youtube/',youtube),
    path('search/',mainsearch),
    path('test/',test),
    path('api/data/',apidata),

    path('api/',include(urls.urlpatterns))




]
