from django.test import TestCase
from pytube import YouTube
# Create your tests here.
import re
req=requests.get("https://aahs.ibomma.pw/ai-n2cdl/spark-2023-nch2i-telugu-movie-watch-online.html")
soup=bs(req.content,'html.parser')
name=soup.find("div",class_="entry-title-movie")
genres=soup.find("article",id="https://aahs.ibomma.pw/ai-n2cdl/spark-2023-nch2i-telugu-movie-watch-online.html")
cast=soup.find("div",class_="cast-and-director")
trailer=soup.find("a",class_="button-trailer-css")
scripts=soup.find_all('script', string=re.compile('lazyIframe.src'))
image=soup.find('img',class_="entry-thumb")
genre=""
for i in scripts:
    match = re.search(r"lazyIframe\.src\s*=\s*'([^']*)'", i.string)
    if match:
        link = match.group(1)
for i in genres.get('class'):
  if "tag-" in i:
    genre+=i.replace("tag-","")+" "

print(name.get_text())
print(genre.title())

print(cast.get_text())
print(trailer.get('href'))
print(link)
print(image.get('data-src'))