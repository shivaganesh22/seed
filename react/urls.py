from django.urls import path
from react.views import *
from api.views import ibomma_fcm
from .all_movies import *
urlpatterns = [
    #movierulz
    path('movierulz/',movierulz),
    path('movierulz/special/<str:id>/<str:slug>/',special),
    path('movierulz/movie/<str:id>/',movierulzmovie),
    # path('movierulz/movie/<str:id>/<str:slug>/',movierulzmovie),
    path('movierulz/search/<str:query>/',movierulzsearch),
    path('addstream/',add_stream),
    path('getstream/',get_stream),

    path('task1/',task1),
    path('task2/',task2),
    path('task3/',task3),
    path('task4/',task4),
    path('task5/<int:id>/',task5),
    path('listdata/<int:id>/',listdata),

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
    path('allmovies/tvshows/<str:id>/',allMoviestvshows),
    path('allmovies/episodes/<str:id>/',allMoviesEpisodes),
    path('allmovies/player/',fetchPlayer),

    #youtube
    path('youtube/',youtube),
    path('y2mate/',y2mate),
    path('y2matedownload/',y2matedownload),


]
