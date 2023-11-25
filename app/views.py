from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from seedr import SeedrAPI
from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime,timedelta
from pytube import YouTube

def home(r):
    a=0
    if "email" in r.COOKIES:
        a=1
    req=requests.get("https://www.1tamilmv.phd")
    soup=bs(req.content,'html.parser')
    items=soup.findAll('p',style="font-size: 13.1px;")[0]
    alinks=items.findAll('a')
    for i in alinks:
        try:
            if '/e/' in i['href']:
                i['href']="/watch/?link="+i['href']
            else:
                i['href']="/movie/?link="+i['href']
        except:
            pass
    return render(r,'index.html',{"a":a,"items":items.prettify()})

def signin(r):
    if "email" in r.COOKIES:
        return redirect('/')
    if r.method=="POST":    
        res=HttpResponseRedirect('/')
        try:
            SeedrAPI(email=r.POST['email'],password=r.POST['password'])
            res.set_cookie('email',r.POST['email'],expires=datetime.now()+timedelta(days=365))
            res.set_cookie('password',r.POST['password'],expires=datetime.now()+timedelta(days=365))
            messages.success(r,"Login Success")
            return res
        except:
            messages.warning(r,"Invalid Details")
    return render(r,'login.html')
def signout(r):
    response = HttpResponseRedirect('/')
    response.delete_cookie('email')
    response.delete_cookie('password')
    messages.success(r,'Logout Success')
    return response
def files(r):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    if r.method=="POST":
        link=r.POST['link']
        res=seedr.add_torrent(link)
        result=""
        if res['result']==True:
            result=f"Added Successfully {res['title']}"
            messages.success(r,result)
        else:
            messages.warning(r,res['result'])
        return redirect('/files')
    drive=seedr.get_drive()
    max=round(drive["space_max"]/1024**3,2)
    used=round(drive["space_used"]/1024**3,2)
    drive=seedr.get_drive()['folders']
    torrents=seedr.get_drive()['torrents']
    return render(r,'folder.html',{"drive":drive,"a":1,"max":max,"used":used,"torrents":torrents})
#player
def player(r,id):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    file=seedr.get_file(id)
    drive=seedr.get_drive()
    max=round(drive["space_max"]/1024**3,2)
    used=round(drive["space_used"]/1024**3,2)
    return render(r,"player.html",{"url":file['url'],"name":file['name'],"a":1,"max":max,"used":used})
def playfolder(r,id):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    files=seedr.get_folder(id)['files']
    for i in files:
        if '.mkv' in i['name'] or '.mp4' in i['name']:
            return player(r,i['folder_file_id'])
#download
def download(r,id):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    file=seedr.get_file(id)['url']
    return redirect(file)
def downloadfolderfile(r,id):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    files=seedr.get_folder(id)['files']
    for i in files:
        if '.mkv' in i['name'] or '.mp4' in i['name']:
            return redirect(seedr.get_file(i['folder_file_id'])['url'])
def deletefolder(r,id):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    try:
        seedr.delete_folder(id)
        messages.success(r,'Deleted Folder')
    except:
        messages.error(r,'Failed to Delete')
    return redirect('/files')
def deletefile(r,id,fid):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    try:
        seedr.delete_file(id)
        messages.success(r,'Deleted File')
    except:
        messages.error(r,'Failed to Delete')
    return redirect(f'/open/{fid}')
def openfolder(r,id):
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    files=seedr.get_folder(id)['files']
    drive=seedr.get_drive()
    max=round(drive["space_max"]/1024**3,2)
    used=round(drive["space_used"]/1024**3,2)
    return render(r,"files.html",{"files":files,"a":1,"max":max,"used":used})

def movie(r):
    a=0
    if "email" in r.COOKIES:
        a=1
    req=requests.get(r.GET.get('link'))
    soup=bs(req.content,'html.parser')
    magnets=soup.findAll('a')
    links=[]
    for i in magnets:
        if i.get_text()=="MAGNET":
            j=i.find_previous_sibling('strong')
            links.append({"name":j.get_text(),"link":i.get('href')})
    items=soup.findAll('img',class_='ipsImage')
    images=[]
    for i in items:
        images.append({"link":i.get('src')})
    return render(r,"movie.html",{"links":links,"a":a,"images":images})
def addtorrent(r):
    link=r.GET.get('link')
    if not "email" in r.COOKIES:
        return redirect('/login')
    seedr=SeedrAPI(email=r.COOKIES['email'],password=r.COOKIES['password'])
    res=seedr.add_torrent(link)
    result=""
    if res['result']==True:
        result=f"Added Successfully {res['title']}"
        messages.success(r,result)
    else:
        messages.warning(r,res['result'])
    return redirect('/files')
def movierulz(r):
    a=0
    if "email" in r.COOKIES:
        a=1
    req=requests.get("https://ww7.5movierulz.gd")
    soup=bs(req.content,'html.parser')
    items=soup.findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        if not "trailer"  in i.a.get('title').lower():
            movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    if r.method=="POST":
        query=r.POST['query'].lower()
        movies.clear()
        req=requests.get(f"https://ww7.5movierulz.gd/?s="+query)
        soup=bs(req.content,'html.parser')
        items=soup.findAll('div',class_='boxed film')
        movies=[]
        for i in items:
            if not "trailer"  in i.a.get('title').lower():
                movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})

    return render(r,'movierulz.html',{"movies":movies,"a":a})
def movierulzmovie(r):
    a=0
    if "email" in r.COOKIES:
        a=1
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

    return render(r,'movierulzmovie.html',{"links":links,"a":a,"details":details})
def youtube(r):
    a=0
    n=0
    name=0
    image=0
    if "email" in r.COOKIES:
        a=1
    if r.method=="POST":
        url=r.POST['query']
        yt = YouTube(url)
        name=yt.title
        image=yt.thumbnail_url
        n=yt.streams.all()
    return render(r,'youtube.html',{"n":n,"name":name,"image":image,"a":a})

def watch(r):
    return HttpResponseRedirect(r.GET['link'])
def mainsearch(r):
    a=0
    if "email" in r.COOKIES:
        a=1
    flag,page,links,title,se=0,0,0,0,[]
    if r.GET.get('q') is not None:
        query=r.GET.get('q')
        page=r.GET.get('page')
        flag=1
    if r.method=="POST":
        query=r.POST['query']
        page="1"
        flag=1
    if flag:
        req=requests.get("https://torrentz2.nz/search?q="+query+"&page="+page)
        soup=bs(req.content,'html.parser')
        title=soup.find('h2').get_text()
        item=soup.find('div',class_='results')
        dl=item.find_all('dl')
        links=[]
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
            page=[]
            for i in pages[1:-1]:
                page.append({"link":i.get('href'),"name":i.get_text()})
            se.append(pages[0].get('href'))
            se.append(pages[-1].get('href'))
        except:
            pass
    return render(r,'search.html',{"page":page,"items":links,"title":title,"a":a,"se":se})

def solidtorrent(r):
    url="https://solidtorrents.to/torrents/skanda-2023-bolly4u-org-pre-dvdrip-hindi-480p-650m-dfa51/6517f35f1b4e7f6abd17bff5/"
    driver=webdriver.Firefox()
    driver.get(url)
    item=driver.page_source
    driver.quit()
    return render(r,'solid.html',{"item":item})