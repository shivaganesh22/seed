from django.urls import path
from api.views import *
urlpatterns = [
    path('movierulz/',movierulz),
    path('movierulz/movie/',movierulzmovie),
]