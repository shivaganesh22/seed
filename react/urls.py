from django.urls import path
from react.views import *
from api.views import ibomma_fcm
urlpatterns = [
    path('movierulz/',movierulz),
    path('movierulz/special/',special),
    path('movierulz/movie/',movierulzmovie),
    path('tamilmv/',tamilmv),
    path('tamilmv/movie/',tamilmvmovie),
    path('login/',LoginApi.as_view()),
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
    path('search/',mainsearch),
    path('movierulz/search/<query>',movierulzsearch),
    path('rename/folder/<id>/',RenameFolder.as_view()),
    path('rename/file/<id>/',RenameFile.as_view()),
    path('youtube/',youtube),
    path('ibomma/movie/',ibommamovie),
    path('ibomma/',ibomma),
    path('sports/',sports),
    path('sports/app/play.php',jioplayer),
    path('sports/player/',sportsplayer),

]
