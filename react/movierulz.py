from django.http import JsonResponse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs

#home
domain="https://ww2.5movierulz.cab/"
def movierulz(r):
    req=requests.get(domain)
    soup=bs(req.content,'html.parser')
    items=soup.find('div',class_='films').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    return JsonResponse({"movies":movies})