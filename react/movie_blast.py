from django.http import JsonResponse
import requests
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup as bs

domain="https://mb.cloud-stream.tech"
headers = {"Authorization": "Bearer jaanuismylove143and143myloveisjaanu"}
def get_data(url):
    res=requests.get(domain+url,headers=headers)
    return res.json() 

def home(r):
    return JsonResponse(get_data("/api/media/mobile/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"))
def pinned(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/pinned/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def top_content(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/topteen/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def recently_added(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/new/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def latest_series_episodes(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/media/seriesEpisodesAll/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def recommended(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/recommended/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def trending(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/trending/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def choosed(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/choosed/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def popular_series(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/popularseries/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def latest_series(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/latestseries/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def next_this_week(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/thisweek/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))


def most_popular(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/popularmovies/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def search(r):
    query=r.GET.get('query','')
    return JsonResponse(get_data(f"/api/search/{query}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"))

def movie_details(r,id):
    return JsonResponse(get_data(f"/api/media/detail/{id}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"))

def series_details(r,id):
    return JsonResponse(get_data(f"/api/series/show/{id}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"))

def genres(r):
    return JsonResponse(get_data("/api/genres/list/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"))

def movies_all(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/movies/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def movies_filter(r):
    page=r.GET.get('page',1)
    sort=r.GET.get('filter','latestadded')
    return JsonResponse(get_data(f"/api/movies/{sort}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def movies_genre(r,id):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/mediaLibrary/show/{id}/movie/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def series_all(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/series/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def series_filter(r):
    page=r.GET.get('page',1)
    sort=r.GET.get('filter','latestadded')
    return JsonResponse(get_data(f"/api/series/{sort}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def series_genre(r,id):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/mediaLibrary/show/{id}/serie/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
