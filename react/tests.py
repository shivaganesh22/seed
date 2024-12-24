from django.test import TestCase
#home page
import requests 
domain="https://mb.cloud-stream.tech"
headers = {
    "Authorization": "Bearer jaanuismylove143and143myloveisjaanu",
   }

response = requests.get("https://mb.cloud-stream.tech/api/media/mobile/jdvhhjv255vghhgdhvfch2565656jhdcghfdf", headers=headers)
print(response.json())