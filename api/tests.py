from django.test import TestCase

# Create your tests here.
import requests
from bs4 import BeautifulSoup as bs

req=requests.get("https://sports-cricstreaming.vercel.app")
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
        item.href='/sports/player/?link='+item.href
        
    }
"""
items.insert(0,sc)
print(items)
