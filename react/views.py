from django.http import JsonResponse
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import html
import requests
from bs4 import BeautifulSoup as bs
from pytube import YouTube
from seedrcc import Login,Seedr
from urllib.parse import urlparse,quote
import time
import re
import base64
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.

domain="https://ww2.5movierulz.cab/"
def movierulz(r):
    req=requests.get(domain)
    soup=bs(req.content,'html.parser')
    items=soup.find('div',class_='films').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":urlparse(i.a.get('href')).path,"image":i.img.get('src')})
    return JsonResponse({"movies":movies})
def movierulzmovie(r,id):
    req=requests.get(domain+id)
    print(domain+id)
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
def movierulzsearch(r,query):
    #req=requests.get(f"https://www.5movierulz.blog/search_movies?s="+query)
    req=requests.get(f"{domain}?s="+query)
    soup=bs(req.content,'html.parser')
    items=soup.find(id='main').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":urlparse(i.a.get('href')).path,"image":i.img.get('src')})
    return JsonResponse({"movies":movies})
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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def send_fcm_notification( title, body,image,link):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAhHqY1L0:APA91bF76GAl0BG_JOc9UNOTmQCBAA8irf_7z9zRRIr7NmvM3Gr4VYYTnHAMLb-ZP-td473Bfjek76dYR81a0xnRRFkPihOeTdA8quIotP8uw685M6ZjZJrL-jokGGreuRywtYd7JdJj',  # Replace YOUR_SERVER_KEY with your Firebase Server key
    }
    payload = {
        'to': '/topics/movies',
        'data': {
            'title': title,
            'body': body,
            'image':image,
            # "icon":"https://rsgmovies.vercel.app/fav_c.png",
            'link':link
        },
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return "Sent "+body
    else:
        return "Failed to sent notification "+body
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
                items.append(send_fcm_notification("Movierulz Movie Update",i['name'],i['image'],'/movierulz/movie'+i['link']))
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
                return Response({'error': "Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class DefaultLogin(APIView):
    def get(self,r):
        try: 
            return Response({"token":"8b564b79a986b849e45e783e87f5dfa4292e4eed","created":False,"status":True})
        except:     
            return Response({"error":"Failed to login"},status=status.HTTP_400_BAD_REQUEST)
class FilesApi(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r):
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        try:
            data=ac.listContents(id)
            data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
            data["files"] = sorted(data['files'], key=lambda x: x['name'])
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({"error":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
    


class OpenFolder(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        try:
            data=ac.listContents(id)
            data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
            data["files"] = sorted(data['files'], key=lambda x: x['name'])
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({"error":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
    

class FolderFile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
            
        try:
            files=ac.listContents(id)['files']
            return Response(ac.fetchFile(files[0]['folder_file_id']),status=status.HTTP_200_OK)
        except:
            return Response({"error":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)

class GetFile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
            
        try:
            
            return Response(ac.fetchFile(id),status=status.HTTP_200_OK)
        except:
            return Response({"error":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
    

class AddTorrent(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        link=r.GET.get('link')
        res=ac.addTorrent(link)
        return Response(res,status=status.HTTP_200_OK)
class DeleteTorrent(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        res=ac.deleteTorrent(id)
        return Response(res,status=status.HTTP_200_OK)
    
class DeleteFolder(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        res=ac.deleteFolder(id)
        return Response(res,status=status.HTTP_200_OK)
    
class DeleteFile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        res=ac.deleteFile(id)
        return Response(res,status=status.HTTP_200_OK)
    
class RenameFolder(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
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
            return  Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
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

def y2mate(r):
    res=requests.post("https://in76.y2mates.com/mates/analyzeV2/ajax",data={"k_query":r.GET["link"]})
    return JsonResponse(res.json())
def y2matedownload(r):
    res=requests.post("https://in76.y2mates.com/mates/convertV2/index",data={"vid":r.GET["vid"],"k":r.GET["link"]})
    return JsonResponse(res.json())
from .models import *
def filter_entries_less_than_2gb(entries):
    def convert_to_gb(size_str):
        try:
            size, unit = size_str.split()
            size = float(size)
            if unit.lower() == 'mb':
                size /= 1024  # Convert MB to GB
            return size
        except:
            pass
    filtered_entries = []

    for entry in entries:
        try:
            ss=entry["name"].split()
            size_str = ss[0] + ' ' + ss[1]
            if convert_to_gb(size_str) < 2 and len(filtered_entries)<=6:
                filtered_entries.append(entry)
        except:
            pass
    return filtered_entries
key="17027hp41jytl2tt72twi"
def delete_all_files(ac):
    data=ac.listContents()
    if data["folders"]:
        ac.deleteFolder(data["folders"][-1]['id'])
    if data["files"]:
        ac.deleteFile(data["files"][-1]['folder_file_id'])
    if data["torrents"]:
        ac.deleteTorrent(data["torrents"][-1]['id'])
    
@api_view(['GET'])
def add_stream(request):
    response=movierulz(request)
    total=0
    items=[]
    try:
        movies=json.loads(response.content)
        new_movies=[]
        seedr=Login("shivaganeshrsg1@gmail.com","Shiva123@")
        response=seedr.authorize()
        ac=Seedr(seedr.token)
        for i in movies['movies']:
            link=i["link"]
            name=i["name"]
            flag=False
            if not StreamLink.objects.filter(slug=i['name']).exists():
                res=movierulzmovie(request,link)
                links=filter_entries_less_than_2gb(json.loads(res.content)["links"])
                if links:
                    for ii in links:
                        delete_all_files(ac)
                        print("uploading")
                        ac.addTorrent(magnetLink=ii["link"])
                        time.sleep(15)
                        data=ac.listContents()
                        if data["torrents"]:
                            time.sleep(15)
                        data=ac.listContents()
                        if data["folders"]:
                            folder=ac.listContents(folderId=data["folders"][-1]["id"])
                            if folder["files"]:
                                file=ac.fetchFile(fileId=folder["files"][-1]["folder_file_id"])
                                url=quote(file["url"])
                                print("adding")
                                req=requests.get(f"https://api.streamwish.com/api/upload/url?key={key}&url={url}")
                                filecode=req.json()["result"]['filecode']
                                while True:
                                    time.sleep(10)
                                    res=requests.get(f"https://api.streamwish.com/api/file/info?key={key}&file_code={filecode}")
                                    print(res.json())
                                    if res.json()['result'][0]['status']!=404:
                                        break
                                print("editing")
                                res=requests.get(f"https://api.streamwish.com/api/file/edit?key={key}&file_code={filecode}&file_title=RSG MOVIES-{name}-{ii['name']}")
                                print("edited",res.json())
                                flag=True
            if flag:
                StreamLink(slug=name).save()
                items.append(name)
                total+=1
        
    except Exception as e :
        print(e)

    return Response({'total':total,"items":items}, status=status.HTTP_200_OK)
@api_view(["GET"])
def get_stream(r):
    req=requests.get(f"https://api.streamwish.com/api/file/list?key={key}&per_page=500")
    data=req.json()
    results=[]
    unique=[]
    if data["result"]["pages"]>1:
        for j in range(1,data["result"]["pages"]+1):
            req=requests.get(f"https://api.streamwish.com/api/file/list?key={key}&page={j}&per_page=500")
            files=req.json()["result"]["files"]
            for i in files:
                if r.GET["link"] in html.unescape(i["title"]):
                    x=i["title"].split('-')[-1]
                    if x not in unique:
                        unique.append(x)
                        results.append({"name":x,"link":i["file_code"]})
    else:
        files=data["result"]["files"]
        for i in files:
                if r.GET["link"] in html.unescape(i["title"]):
                    x=i["title"].split('-')[-1]
                    if x not in unique:
                        unique.append(x)
                        results.append({"name":x,"link":i["file_code"]})
    return JsonResponse({"movies":results})
emails=["shivaganeshrsg1@gmail.com","tolokox424@lisoren.com","wanapil403@luravell.com","bepimo8558@dovinou.com","ribix96778@luravell.com","yohivob255@exeneli.com"]
def login_accounts(id):
    seedr=Login(emails[id],"Shiva123@")
    response=seedr.authorize()
    return Seedr(seedr.token)

@api_view(['GET'])
def task1(request):
    response=movierulz(request)
    op=""
    try:
        movies=json.loads(response.content)
        for i in movies['movies']:
            link=i["link"]
            name=i["name"]
            if not StreamLink.objects.filter(slug=i['name']).exists():
                res=movierulzmovie(request,link)
                links=filter_entries_less_than_2gb(json.loads(res.content)["links"])
                if links:
                    stream_link,created=StreamLink.objects.get_or_create(slug=name)
                    for i in range(len(links)):
                        EachStream.objects.create(movie=stream_link,link=links[i]["link"],name=links[i]["name"],account=i)
                    op+="added "+name
                    break
                else:
                    op+="no stream"+name
    except Exception as e :
        print(e)
    return Response({'status':True,"op":op}, status=status.HTTP_200_OK)
@api_view(["GET"])
def task2(request):
    op=""
    try:
        data=EachStream.objects.filter(is_uploaded=False).first()
        if data:
            k=EachStream.objects.filter(is_uploaded=True,account=data.account).first()
            if not k:
                ac=login_accounts(data.account)
                delete_all_files(ac)
                data.is_uploaded=True
                data.save()
                op+="uploading "
                ac.addTorrent(magnetLink=data.link)
                op+="uploaded "+data.name
            else:
                op+="already exists "+k.movie.slug+" "+k.name
        else:
            op+="no data"
    except Exception as e :
        print(e)
        op+="error "+str(e) 
    return Response({'status':True,"op":op}, status=status.HTTP_200_OK)

@api_view(["GET"])
def task3(request):
    op=""
    try:
        obj=EachStream.objects.filter(is_uploaded=True,is_edited=False).first()
        if obj:
            ac=login_accounts(obj.account)
            data=ac.listContents()
            if data["folders"]:
                folder=ac.listContents(folderId=data["folders"][-1]["id"])
                if folder["files"]:
                    file=ac.fetchFile(fileId=folder["files"][-1]["folder_file_id"])
                    url=quote(file["url"])
                    op+="uploading"
                    req=requests.get(f"https://api.streamwish.com/api/upload/url?key={key}&url={url}")
                    filecode=req.json()["result"]['filecode']
                    obj.link=filecode
                    obj.is_edited=True
                    obj.save()
                    op+="uploaded"+obj.movie.slug+" "+obj.name
                # elif len(folder["files"])>1:
                #     for i in folder["files"]:
                #         file=ac.fetchFile(fileId=i["folder_file_id"])
                #         url=quote(file["url"])
                #         op+="uploading"
                #         req=requests.get(f"https://api.streamwish.com/api/upload/url?key={key}&url={url}")
                #         filecode=req.json()["result"]['filecode']
                #         EachStream.objects.create(movie=obj.movie,link=filecode,name=file["name"],account=obj.account,is_uploaded=True,is_edited=True)
                #         op+="uploaded"+obj.movie.slug+" "+obj.name+" "+file["name"]
                #     obj.delete()
            else:
                op+="folder not exists"+obj.movie.slug+" "+obj.name
        else:
            op+="no data"
    except Exception as e :
        print(e)
        op+="error "+str(e)
    return Response({'status':True,"op":op}, status=status.HTTP_200_OK)
@api_view(["GET"])
def task4(request):
    op=""
    try:
        obj=EachStream.objects.filter(is_edited=True).first()
        if obj:
            op+="editing "
            res=requests.get(f"https://api.streamwish.com/api/file/info?key={key}&file_code={obj.link}")          
            if res.json()['result'][0]['status']!=404: 
                print("s")
                res=requests.get(f"https://api.streamwish.com/api/file/edit?key={key}&file_code={obj.link}&file_title=RSG MOVIES-{obj.movie.slug}-{obj.name}")
                op+="edited "+obj.movie.slug+" "+obj.name
                obj.delete()
            else:
                op+="not uploaded"+obj.movie.slug+" "+obj.name
        else:
            op+="no data"
    except Exception as e :
        print(e)
        op+="error "+str(e)
    return Response({'status':True,"op":op}, status=status.HTTP_200_OK)