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
    path('folder/getlink/<id>',getfolderlink),
    

]