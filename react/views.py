from django.http import JsonResponse
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from bs4 import BeautifulSoup as bs
from pytube import YouTube
from seedrcc import Login,Seedr
import re
import base64
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.
def movierulz(r):
    req=requests.get("https://ww2.5movierulz.cab")
    soup=bs(req.content,'html.parser')
    items=soup.find('div',class_='films').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    return JsonResponse({"movies":movies})
def movierulzmovie(r):
    req=requests.get(r.GET.get('link'))
    soup=bs(req.content,'html.parser')
    items=soup.findAll('a',class_='mv_button_css')
    links=[]
    for i in items:
        #b=i.find('small')
        #links.append({"name":b.get_text(),"link":i.get('href')})
        b=i.findAll('small')
        links.append({"name":b[0].get_text()+" "+b[1].get_text(),"link":i.get('href')})
    items=soup.findAll('p')
    details={}
    details["name"]=soup.find('h2',class_='entry-title').get_text()
    for i in items:
        if "directed" in i.get_text().lower():
            inflinks=i.findAll('a')
            for m in inflinks:
                m['href']="/movierulz/special/?link="+m['href']
            details["inf"]=i.prettify()
            j=i.find_next_sibling()
            details["desc"]=j.prettify()
    details["image"]=soup.find('img',class_='attachment-post-thumbnail').get('src')
    return JsonResponse({"links":links,"details":details})
def special(r):
    req=requests.get(r.GET['link'])
    soup=bs(req.content,'html.parser')
    items=soup.find('div',class_='films').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    return JsonResponse({"movies":movies})
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



@api_view(['POST'])
def contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'true'}, status=status.HTTP_200_OK)
    return Response({'status': 'false'}, status=status.HTTP_401_UNAUTHORIZED)
def send_fcm_notification( title, body,image,link):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAhHqY1L0:APA91bF76GAl0BG_JOc9UNOTmQCBAA8irf_7z9zRRIr7NmvM3Gr4VYYTnHAMLb-ZP-td473Bfjek76dYR81a0xnRRFkPihOeTdA8quIotP8uw685M6ZjZJrL-jokGGreuRywtYd7JdJj',  # Replace YOUR_SERVER_KEY with your Firebase Server key
    }
    payload = {
        'to': '/topics/movies',
        'data': {  # Use 'data' instead of 'notification'    
            'link': link,
        },
        'notification': {
            'title': title,
            'body': body,
            'image':image,
        },
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return "Sent "+body
    else:
        return "Failed to sent notification "+response.body
from app.models import *
@api_view(['GET'])
def movierulz_fcm(request):
    response=movierulz(request)
    total=0
    items=[]
    try:
        data=json.loads(response.content)
        
        new_movies=[]
        for i in data['movies']:
            new_movies.append(Movierulz(name=i['name'],image=i['image'],link=i['link']))
            if not  Movierulz.objects.filter(name=i['name']).exists():
                items.append(send_fcm_notification("Movierulz Movie Update",i['name'],i['image'],'/movierulz/movie?link='+i['link']))
                total+=1
        Movierulz.objects.all().delete()
        Movierulz.objects.bulk_create(new_movies)
    except Exception as e :
        print(e)

    return Response({'total':total,"items":items}, status=status.HTTP_200_OK)

@api_view(['GET'])
def test_fcm(request):
    res=send_fcm_notification("test","test1","iam","lin")
    return Response({"items":res}, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def addFCM(request):
    serializer=FCM_tokenSerializer(FCM_token.objects.all(),many=True)
    if request.method=="POST":
        serializer = FCM_tokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'true'}, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.generics import GenericAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
class FCMList(ListCreateAPIView):
    queryset=FCM_token.objects.all()
    serializer_class=FCM_tokenSerializer
    
class FCMManage(RetrieveUpdateDestroyAPIView):
    queryset=FCM_token.objects.all()
    serializer_class=FCM_tokenSerializer
  

def getSeedr(r):
    seedr=Login(r.auth.user.email,r.auth.user.password)
    response=seedr.authorize()
    try:
        ac=Seedr(seedr.token)
        return ac
    except:
        return None
class LoginApi(APIView):
    def post(self,r):
        serializer=UserSerializer(data=r.data)
        if serializer.is_valid():
            seedr=Login(serializer.validated_data["email"],serializer.validated_data["password"])
            response=seedr.authorize()
            try:
                Seedr(token=seedr.token)
                if User.objects.filter(email=serializer.validated_data["email"],password=serializer.validated_data["password"]):
                    user=User.objects.get(email=serializer.validated_data["email"],password=serializer.validated_data["password"])
                    token,created=Token.objects.get_or_create(user=user)
                    return Response({"token":token.key,"created":created,"status":True})
                user=User.objects.create(username=serializer.validated_data["email"]+" "+serializer.validated_data["password"],email=serializer.validated_data["email"],password=serializer.validated_data["password"])
                token,created=Token.objects.get_or_create(user=user)
                return Response({"token":token.key,"created":created,"status":True})
            except:
                return Response({'status': False},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors)
class FilesApi(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r):
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":False},status=status.HTTP_401_UNAUTHORIZED)
        try:
            data=ac.listContents(id)
            data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
            data["files"] = sorted(data['files'], key=lambda x: x['name'])
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
    


class OpenFolder(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":False},status=status.HTTP_401_UNAUTHORIZED)
        try:
            data=ac.listContents(id)
            data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
            data["files"] = sorted(data['files'], key=lambda x: x['name'])
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
    

class FolderFile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            files=ac.listContents(id)['files']
            return Response(ac.fetchFile(files[0]['folder_file_id']),status=status.HTTP_200_OK)
        except:
            return Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)

class GetFile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            
            return Response(ac.fetchFile(id),status=status.HTTP_200_OK)
        except:
            return Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
    

class AddTorrent(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
        link=r.GET.get('link')
        res=ac.addTorrent(link)
        return Response(res,status=status.HTTP_200_OK)
class DeleteTorrent(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
        res=ac.deleteTorrent(id)
        return Response(res,status=status.HTTP_200_OK)
    
class DeleteFolder(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
        res=ac.deleteFolder(id)
        return Response(res,status=status.HTTP_200_OK)
    
class DeleteFile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
        res=ac.deleteFile(id)
        return Response(res,status=status.HTTP_200_OK)
    
class RenameFolder(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
        name=r.GET['name']
        res=ac.renameFolder(id,name)
        if res['result']:
            return Response(res,status=status.HTTP_200_OK)
        else:
            return Response({"error":res['error'].title()},status=status.HTTP_401_UNAUTHORIZED)
    
class RenameFile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"status":"false"},status=status.HTTP_401_UNAUTHORIZED)
        name=r.GET['name']
        res=ac.renameFile(id,name)
        if res['result']:
            return Response(res,status=status.HTTP_200_OK)
        else:
            return Response({"error":res['error'].title()},status=status.HTTP_401_UNAUTHORIZED)
    



def mainsearch(r):
    req=requests.get("https://torrentz2.nz/search?q="+r.GET['q']+"&page="+r.GET['page'])
    soup=bs(req.content,'html.parser')
    title=soup.find('h2').get_text()
    item=soup.find('div',class_='results')
    dl=item.find_all('dl')
    links=[]
    ends=[]
    page=[]
    for i in dl:
        try:
            url=i.dt.a.get('href')
            name=i.dt.a.get_text()
            span=i.find_all('span')
            magnet=span[0].a.get('href')
            date=span[1].get_text()
            size=span[2].get_text()
            links.append({"name":name,"url":url,"link":magnet,"date":date,"size":size})
        except:
            pass
    try:
        pages=soup.find('div',class_="pagination").find_all('a')
        for i in pages[1:-1]:
            page.append({"link":i.get('href'),"name":i.get_text()})
        ends.append(pages[0].get('href'))
        ends.append(pages[-1].get('href'))
    except:
        pass
    return JsonResponse({"name":title,"links":links,"ends":ends,"pages":page})

def movierulzsearch(r,query):
    #req=requests.get(f"https://www.5movierulz.blog/search_movies?s="+query)
    req=requests.get(f"https://ww2.5movierulz.cab/?s="+query)
    soup=bs(req.content,'html.parser')
    items=soup.find(id='main').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    return JsonResponse({"movies":movies})
def youtube(r):
    url=r.GET['link']
    yt = YouTube(url)
    data={}
    data['title']=yt.title
    data['thumb']=yt.thumbnail_url
    videos=[]
    audio=[]
    for i in yt.streams.all():
        if "video" in i.type:
            videos.append({"audio":i.is_progressive,"codec":i.video_codec.split('.')[0][:-1],"resolution":i.resolution,"size":i.filesize_mb,"url":i.url})
        if "audio" in i.type:
            audio.append({"codec":i.audio_codec.split('.')[0],"resolution":i.abr,"size":i.filesize_mb,"url":i.url})
    data['videos']=videos
    data['audio']=audio
    return JsonResponse(data)
def ibomma(r):
    req=requests.get("https://aahs.ibomma.pw/telugu-movies/")
    soup=bs(req.content,'html.parser')
    items=soup.find_all('article')
    movies=[]
    for i in items:
        try:
            movies.append({"name":i.h2.a.get_text(),"image":base64.b64encode(requests.get(i.img.get('data-src')).content).decode('utf-8'),"link":i.a.get('href')})
        except:
            pass
    return JsonResponse({"movies":movies})

def ibommamovie(r):
    req=requests.get(r.GET['link'])
    soup=bs(req.content,'html.parser')
    name=soup.find("div",class_="entry-title-movie")
    genres=soup.find("article",id=r.GET['link'])
    cast=soup.find("div",class_="cast-and-director")
    director=soup.find("div",class_="movies-director")
    description=soup.find("div",class_="additional-info")
    trailer=soup.find("a",class_="button-trailer-css")
    scripts=soup.find_all('script', string=re.compile('lazyIframe.src'))
    image=soup.find('img',class_="entry-thumb")
    genre=""
    link=""
    details={}
    for i in scripts:
        match = re.search(r"lazyIframe\.src\s*=\s*'([^']*)'", i.string)
        if match:
            link = match.group(1)
    for i in genres.get('class'):
        if "tag-" in i:
            genre+=i.replace("tag-","")+" "
    details["name"] = name.get_text()
    details["genre"] = genre.title()
    details["cast"] = cast.get_text()
    details["director"] = director.get_text()
    details["desc"] = description.get_text()
    details["trailer"] = trailer.get('href')
    details["image"] =base64.b64encode(requests.get(image.get('data-src')).content).decode('utf-8')
    details["link"] = link
    details["dlink"] = r.GET['link']
    return JsonResponse(details)
def sports(r):
    req=requests.get("https://sports-cricstreaming.pages.dev")
    soup=bs(req.content,'html.parser')
    items=soup.find('head')
    sc=soup.new_tag('script')
    sc.string="""
 tt = document.querySelector(".btn-11");
    tt.remove()
    items=document.getElementsByTagName("a")
    for(i=0;i<items.length;i++){
        item=items[i]
        if (item.href.includes("telegram")) item.remove()
        else if (item.href.includes("cricstreaming"))
        item.href="/api/sports/player/?link="+item.href
        
    }
"""
    items.append(sc)
    return render(r,'api/sports.html',{"items":items.prettify()})
def tv(r):
    req=requests.get("https://tata-web-by-krotos.vercel.app")
    soup=bs(req.content,'html.parser')
    header=soup.find('header')
    header.extract()
    soup.find('style').extract()
    soup.find(id='loading-msg').extract()
    dropdown = soup.find(id='channel-dropdown')
    new_option = soup.new_tag('option', value='regional telugu', selected=True)
    new_option.string = 'Regional Telugu' 
    dropdown.insert(0,new_option)
    dropdown.insert_after(soup.new_tag('br'))
    dropdown.insert_after(soup.new_tag('br'))
    links=soup.find_all('a',class_='site-card')
    for i in links:
        i['href']='/tv/tata/player/?link='+i['href']
    return render(r,'api/sports.html',{"tata":soup.prettify()})
def jioplayer(r):
    return redirect(f"https://sports247.eu.org/api/app/play.php?cid={r.GET['cid']}&id={r.GET['id']}")
def sportsplayer(r):
    req=requests.get(r.GET['link'])
    soup=bs(req.content,'html.parser')
    items=soup.find('script').prettify()
    return render(r,'api/sportsplayer.html',{"items":items})
