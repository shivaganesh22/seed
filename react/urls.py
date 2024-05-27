from django.urls import path
from react.views import *
from api.views import ibomma_fcm
from .all_movies import *
urlpatterns = [
    #movierulz
    path('movierulz/',movierulz),
    path('movierulz/special/',special),
    path('movierulz/movie/<str:id>/',movierulzmovie),
    path('movierulz/search/<str:query>/',movierulzsearch),

    path('tamilmv/',tamilmv),
    path('tamilmv/movie/<str:id>/',tamilmvmovie),

    path('login/',LoginApi.as_view()),
    path('login/default/',DefaultLogin.as_view()),

    path('contact/',contact),

    path('fcm/',FCMList.as_view()),
    path('fcm/<pk>',FCMManage.as_view()),
    path('movierulz_fcm/',movierulz_fcm),
    path('ibomma_fcm/',ibomma_fcm),
    path('test_fcm/',test_fcm),

    path('files/',FilesApi.as_view()),
    path('open/<id>',OpenFolder.as_view()),
    path('folder/file/<id>',FolderFile.as_view()),
    path('file/<id>',GetFile.as_view()),
    path('addtorrent/',AddTorrent.as_view()),
    path('deletetorrent/<id>',DeleteTorrent.as_view()),
    path('deletefolder/<id>',DeleteFolder.as_view()),
    path('deletefile/<id>',DeleteFile.as_view()),
    path('rename/folder/<id>/',RenameFolder.as_view()),
    path('rename/file/<id>/',RenameFile.as_view()),

    path('search/',mainsearch),
    


    path('youtube/',youtube),

    path('ibomma/movie/',ibommamovie),
    path('ibomma/',ibomma),

    path('sports/',sports),
    path('sports/app/play.php',jioplayer),
    path('sports/player/',sportsplayer),

    #allmovies
    path('allmovies/',allMovies),
    path('imdb/',imdbMovies),
    path('allmovies/search/',allMoviesSearch),
    path('allmovies/all/',allMoviesLink),
    path('allmovies/movies/<str:id>/',allMoviesMovie),


]
