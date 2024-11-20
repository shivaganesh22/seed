from django.test import TestCase
import requests
req=requests.get("https://ww18.4movierulz.io/")
print(req.status_code)
# print(req.request.headers)