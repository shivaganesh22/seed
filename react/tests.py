from django.test import TestCase

# Create your tests here.
import requests
key="56925fxislvf4q1zn2qfp"
url="https://rs15.seedr.cc/ff_get/5448096856/www.5MovieRulz.loan%20-%20Indrani%20(2024)%20720p%20Telugu%20DVDScr%20-%20x264%20-%20AAC%20-%201.4GB.mkv?st=duAaifLWQolv4AIjm5kRGQ&e=1718688638"
req=requests.get(f"https://filemoonapi.com/api/remote/add?key={key}&url={url}")
print(req.json())
