from django.test import TestCase

# Create your tests here.
import requests
url="https://seed-ten.vercel.app/api/folder/getlink/487767777"
res=requests.post(url,data={"email":"rockstarshivaganesh@gmail.com","password":"Shiva123@"})
print(res.json())