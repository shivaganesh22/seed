from django.urls import path
from api.views import *
urlpatterns = [
    path('movierulz/',movierulz),
    path('movierulz/movie/',movierulzmovie),
    path('tamilmv/',tamilmv),
    path('tamilmv/movie/',tamilmvmovie),
    path('login/',signin),
    path('files/',files),
    path('open/<id>',openfolder),
    path('folder/file/<id>',folderfile),
    path('file/<id>',getFile),
    path('addtorrent/',addtorrent),
    path('deletetorrent/<id>',deletetorrent),
    path('deletefolder/<id>',deletefolder),
    path('deletefile/<id>',deletefile),
    path('search/',mainsearch),
    path('movierulz/search/<query>',movierulzsearch),
    path('rename/folder/<id>/',renamefolder),
    path('rename/file/<id>/',renamefile),
    path('youtube/',youtube),
    path('ibomma/movie/',ibommamovie),
    path('ibomma/',ibomma),
    path('sports/',sports),
    path('sports/player/',sportsplayer),

]
