from django.test import TestCase

# Create your tests here.
import requests
url="https://fictional-meme-xx7wvg54g54c69x4-8000.app.github.dev/api/open/487767777"
res=requests.post(url,data={"email":"rockstarshivaganesh@gmail.com","password":"Shiva123@"})
print(res.json())