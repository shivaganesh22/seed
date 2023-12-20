from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup as bs
from seedrcc import Login,Seedr

# Create your views here.
def movierulz(r):
    req=requests.get("https://ww7.5movierulz.gd")
    soup=bs(req.content,'html.parser')
    items=soup.findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        if not "trailer"  in i.a.get('title').lower():
            movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    return JsonResponse({"movies":movies})
def movierulzmovie(r):
    req=requests.get(r.GET.get('link'))
    soup=bs(req.content,'html.parser')
    items=soup.findAll('a',class_='mv_button_css')
    links=[]
    for i in items:
        b=i.findAll('small')
        links.append({"name":b[0].get_text()+" "+b[1].get_text(),"link":i.get('href')})
    items=soup.findAll('p')
    details={}
    details["name"]=soup.find('h2',class_='entry-title').get_text()
    for i in items:
        if "directed" in i.get_text().lower():
            details["inf"]=i.prettify()
            j=i.find_next_sibling()
            details["desc"]=j.prettify()
    details["image"]=soup.find('img',class_='attachment-post-thumbnail').get('src')
    return JsonResponse({"links":links,"details":details})
def tamilmv(r):
    req=requests.get("https://www.1tamilmv.phd")
    soup=bs(req.content,'html.parser')
    items=soup.findAll('p',style="font-size: 13.1px;")[0]
    alinks=items.findAll('a')
    for i in alinks:
        try:
            if '/e/' in i['href']:
                i['href']="/doodplay/?link="+i['href']
            else:
                i['href']="/tamilmv/movie/?link="+i['href']
        except:
            pass
    return JsonResponse({"items":items.prettify()})
def tamilmvmovie(r):
    req=requests.get(r.GET.get('link'))
    soup=bs(req.content,'html.parser')
    magnets=soup.findAll('a')
    links=[]
    for i in magnets:
        try:
            if i.get_text()=="MAGNET" or i.find('img').get('alt')=="magnet.png":
                j=i.find_previous_sibling('strong')
                links.append({"name":j.get_text(),"link":i.get('href')})
        except:
            pass
    items=soup.findAll('img',class_='ipsImage')
    images=[]
    for i in items:
        images.append({"link":i.get('src')})
    return JsonResponse({"links":links,"images":images})
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCredentialsSerializer

@api_view(['POST'])
def signin(request):
    serializer = UserCredentialsSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def getSeedr(r):
    email=r.headers.get("email")
    password=r.headers.get("password")
    seedr=Login(r.COOKIES['email'],r.COOKIES['password'])
    response=seedr.authorize()
    return Seedr(seedr.token)

def files(r):
    ac=getSeedr(r)
    data=ac.listContents()
    data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
    return JsonResponse(data)
