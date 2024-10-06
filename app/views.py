from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from seedrcc import Login,Seedr
import re
from bs4 import BeautifulSoup as bs
from .forms import *
import requests
from datetime import datetime,timedelta
from pytube import YouTube

#tamilmv
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
    return render(r,'index.html',{"items":items.prettify()})


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
    return render(r,"movie.html",{"links":links,"images":images})

def doodplay(r):
    return HttpResponseRedirect(r.GET['link'])

#movierulz
def movierulz(r):
    query=0
    req=requests.get("https://www.5movierulz.skin/")
    soup=bs(req.content,'html.parser')
    items=soup.find('div',class_='films').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    if r.method=="POST":
        query=r.POST['query'].lower()
        movies.clear()
        req=requests.get(f"https://www.5movierulz.skin/search_movies?s="+query)
        # req=requests.get(f"https://www.5movierulz.skin/?s="+query)
        soup=bs(req.content,'html.parser')
        items=soup.find(id='main').findAll('div',class_='boxed film')
        movies=[]
        for i in items:
            movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    return render(r,'movierulz.html',{"movies":movies,"query":query})
#movierulz
def special(r):
    query=0
    link=r.GET['link']
    req=requests.get(link)
    soup=bs(req.content,'html.parser')
    items=soup.find('div',class_='films').findAll('div',class_='boxed film')
    movies=[]
    for i in items:
        movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    if r.method=="POST":
        query=r.POST['query'].lower()
        movies.clear()
        req=requests.get(f"https://www.5movierulz.blog/search_movies?s="+query)
        soup=bs(req.content,'html.parser')
        items=soup.find(id='main').findAll('div',class_='boxed film')
        movies=[]
        for i in items:
            movies.append({"name":i.a.get('title'),"link":i.a.get('href'),"image":i.img.get('src')})
    return render(r,'movierulz.html',{"movies":movies,"query":query})

def movierulzmovie(r):
    req=requests.get(r.GET.get('link'))
    soup=bs(req.content,'html.parser')
    items=soup.findAll('a',class_='mv_button_css')
    links=[]
    for i in items:
        b=i.find('small')
        links.append({"name":b.get_text(),"link":i.get('href')})
        # b=i.findAll('small')
        # links.append({"name":b[0].get_text()+" "+b[1].get_text(),"link":i.get('href')})
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
    return render(r,'movierulzmovie.html',{"links":links,"details":details})


def signin(r):
    if "email" in r.COOKIES:
        return redirect('/')
    if r.method=="POST":    
        res=HttpResponseRedirect('/')
        seedr=Login(r.POST['email'],r.POST['password'])
        response=seedr.authorize()
        try:
            Seedr(token=seedr.token)
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

#youtube downloader
def youtube(r):
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
    return render(r,'youtube.html',{"n":n,"name":name,"image":image})
#search
def mainsearch(r):
    flag,page,links,title,query,se=0,0,0,0,0,[]
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
    return render(r,'search.html',{"page":page,"items":links,"title":title,"query":query,"se":se})

#seedr
def getSeedr(r):
    if "email" in r.COOKIES:
        seedr=Login(r.COOKIES['email'],r.COOKIES['password'])
        response=seedr.authorize()
        return Seedr(seedr.token)
    else:
        return None
def apidata(r):
    ac=getSeedr(r)
    data=ac.listContents()
    data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
    return JsonResponse(data)

def folders(r):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    if r.method=="POST":
        link=r.POST['link']
        res=ac.addTorrent(link)
        if res['result']==True:
            messages.success(r,f'Added Successfully {res["title"]}')
        else:
            messages.warning(r,res['result'])
        return redirect('/files')
    content=ac.listContents()
    return render(r,'folder.html',{"content":content})

def addtorrent(r):
    link=r.GET.get('link')
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    res=ac.addTorrent(link)
    if res['result']==True:
        messages.success(r,f'Added Successfully {res["title"]}')
    else:
        messages.warning(r,res['result'])
    return redirect('/files')

def deletetorrent(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    try:
        ac.deleteTorrent(id)
        messages.success(r,'Deleted Torrent')
    except:
        messages.error(r,'Failed to Delete')
    return redirect('/files')

def openfolder(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    if r.method=="POST":
        link=r.POST['link']
        res=ac.addTorrent(link)
        if res['result']==True:
            messages.success(r,f'Added Successfully {res["title"]}')
        else:
            messages.warning(r,res['result'])
        return redirect('/files')
    content=ac.listContents(id)
    return render(r,"files.html",{"content":content})

def deletefolder(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    try:
        ac.deleteFolder(id)
        messages.success(r,'Deleted Folder')
    except:
        messages.error(r,'Failed to Delete')
    return redirect('/files')

def renamefolder(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    name=r.GET['name']
    res=ac.renameFolder(id,name)
    if res['result']:
        messages.success(r,"Renamed Success")
    else:
        messages.warning(r,res['error'].title())
    return redirect("/files")

#player
def player(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    file=ac.fetchFile(id)
    return render(r,"player.html",{"file":file,"content":ac.listContents()})
def playfolder(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    files=ac.listContents(id)['files']
    try:
        i=files[0]
        return player(r,i['folder_file_id'])
    except:
        messages.warning(r,'No File')
        return redirect('/files')
    return redirect('/files')
#download
def download(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    file=ac.fetchFile(id)['url']
    return redirect(file)
def downloadfolderfile(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    files=ac.listContents(id)['files']
    try:
        i=files[0]
        return redirect(ac.fetchFile(i['folder_file_id'])['url'])
    except:
        messages.warning(r,'No File')
        return redirect('/files')
    return redirect('/files')
def deletefile(r,id,fid):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    try:
        ac.deleteFile(id)
        messages.success(r,'Deleted File')
    except:
        messages.error(r,'Failed to Delete')
    return redirect(f'/open/{fid}')

def renamefile(r,fid,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    name=r.GET['name']
    res=ac.renameFile(id,name)
    if res['result']:
        messages.success(r,"Renamed Success")
    else:
        messages.warning(r,res['error'].title())
    return redirect(f'/open/{fid}')
def renamefilehome(r,id):
    ac=getSeedr(r)
    if not ac:
        return redirect('/login')
    name=r.GET['name']
    res=ac.renameFile(id,name)
    if res['result']:
        messages.success(r,"Renamed Success")
    else:
        messages.warning(r,res['error'].title())
    return redirect(f'/files')

def ibomma(r):
    req=requests.get("https://aahs.ibomma.pw/telugu-movies/")
    soup=bs(req.content,'html.parser')
    items=soup.find_all('article')
    movies=[]
    for i in items:
        try:
            movies.append({"name":i.h2.a.get_text(),"image":i.img.get('data-src'),"link":i.a.get('href')})
        except:
            pass
    return render(r,"ibomma.html",{"movies":movies})

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
    details["image"] = image.get('data-src')
    details["link"] = link
    details["dlink"] = r.GET['link']
    return render(r,"ibommamovie.html",{"details":details})
def sports(r):
    req=requests.get("https://sport-cricstreaming.vercel.app/")
    soup=bs(req.content,'html.parser')
    # items=soup.find('head').prettify()
    return render(r,'sports.html',{"items":soup.prettify()})
def sportsplayer(r):
    req=requests.get(r.GET['link'])
    soup=bs(req.content,'html.parser')
    # items=soup.find('script').prettify()
    return render(r,'sportsplayer.html',{"items":soup.prettify()})
def contact(r):
    form=ContactForm()
    if r.method=="POST":
        form=ContactForm(r.POST)
        if form.is_valid():
            form.save()
            messages.success(r,'Form Submitted')
            return redirect('/')
    return render(r,'contact.html',{"form":form})


def tv(r):
    req=requests.get("https://sport-cricstreaming.vercel.app/")
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
    return render(r,'tv.html',{"tata":soup.prettify()})
def tataplayer(r):
    return redirect('https://tata-web-by-krotos.vercel.app/'+r.GET['link'])
def jioplayer(r):
    return redirect(f"https://sports247.eu.org/api/app/play.php?cid={r.GET['cid']}&id={r.GET['id']}")
def test(r):
    return render(r,'test.html')
def privacy(r):
    return render(r,'privacy.html')
