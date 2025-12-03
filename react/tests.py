from django.test import TestCase
#home page
import requests 
domain="https://mb.cloud-stream.tech"
headers = {
    "Authorization": "Bearer jaanuismylove143and143myloveisjaanu",
   }

response = requests.get("https://app.cloud-mb.xyz/api/media/detail/1753/jdvhhjv255vghhgdhvfch2565656jhdcghfdf", )
print(response.json())