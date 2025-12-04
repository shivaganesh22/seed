from django.http import JsonResponse
import requests
import random
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup as bs

domain="https://app.cloud-mb.xyz"
headers = {"Authorization": "Bearer jaanuismylove143and143myloveisjaanu"}
PROXY_LIST = [
"142.111.48.253:7030",
"31.59.20.176:6754",
"23.95.150.145:6114",
"198.23.239.134:6540",
"107.172.163.27:6543",
"198.105.121.200:6462",
"64.137.96.74:6641",
"84.247.60.125:6095",
"216.10.27.159:6837",
"142.111.67.146:5611",
  
]

USER = "fqjdeeqq"
PASS = "r63dies6krlg"
def get_data(url):
    chosen_ip = random.choice(PROXY_LIST)
    formatted_proxy = f"http://{USER}:{PASS}@{chosen_ip}"
    
    proxies = {
        "http": formatted_proxy,
        "https": formatted_proxy,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    res=requests.get(domain+url,headers=headers,proxies=proxies)
    return res.json() 

def home(r):
    return JsonResponse(get_data("/api/media/mobile/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"))
def pinned(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/pinned/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
def new_hd(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/media/names/New%20HD%20Released/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))
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
def latest_movies(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/latestmovies/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def next_this_week(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/thisweek/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))


def most_popular(r):
    page=r.GET.get('page',1)
    return JsonResponse(get_data(f"/api/genres/popularmovies/all/jdvhhjv255vghhgdhvfch2565656jhdcghfdf?page={page}"))

def search(r):
    query=r.GET.get('query','')
    return JsonResponse(get_data(f"/api/search/{query}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"))

def movie_details(request, id):
    path = f"/api/media/detail/{id}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"
    chosen_ip = random.choice(PROXY_LIST)
    formatted_proxy = f"http://{USER}:{PASS}@{chosen_ip}"
    
    proxies = {
        "http": formatted_proxy,
        "https": formatted_proxy,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(domain+path, headers=headers, proxies=proxies)
        # response = requests.get(domain+path, headers=headers, )
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({"error": "Failed to fetch"}, status=500)
def series_details(r,id):
    path=f"/api/series/show/{id}/jdvhhjv255vghhgdhvfch2565656jhdcghfdf"
    chosen_ip = random.choice(PROXY_LIST)
    formatted_proxy = f"http://{USER}:{PASS}@{chosen_ip}"
    
    proxies = {
        "http": formatted_proxy,
        "https": formatted_proxy,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(domain+path, headers=headers, proxies=proxies)
        # response = requests.get(domain+path, headers=headers,)
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({"error": "Failed to fetch"}, status=500)

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
