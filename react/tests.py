from django.test import TestCase

# Create your tests here.
import requests
from urllib.parse import urlparse,quote
# auth_token="o+FReHCGQi8VUIYRGZ8Mqyn5lAsRWTiQY8LujIZCYkk="
auth_token="k1nkbA6NJbsR+lq2HidFz7y670h4f1wCBLWDWjJuiiM="
import requests
import json
import time

# Define the URL and the authorization token
# url = "https://api.cron-job.org/jobs"


# # Define the job data

# for i in range(2,6):
#     l=[5,10,15,20,25,30]
#     job_data = {
#     "job": {
#         "url": "https://rsg-movies.vercel.app/react/task3/",
#         "enabled": False,
#         "title":"task 3",
#         "saveResponses": True,
#         "schedule": {
#             "timezone": "Europe/Berlin",
#             "expiresAt": 0,
#             "hours": [19],    # 0 for 12 AM
#             "mdays": [-1],   # Every day
#             "minutes": [l[i]],  # 5 minutes past the hour
#             "months": [-1],  # Every month
#             "wdays": [-1]    # Every weekday
#         }
#     }
# }

# # Make the PUT request
#     response = requests.put(
#         url,
#         headers={
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {auth_token}'
#         },
#         data=json.dumps(job_data)
#     )
#     if response.status_code == 200:
#         print("Job scheduled successfully")
#     else:
#         print(f"Failed to schedule job: {response.status_code}")
#         print(response.text)
#     time.sleep(1)

# Check the response
key="17027hp41jytl2tt72twi"
url="magnet:?xt=urn:btih:8f1f7793f7e0ec0f8f653e7abac3fecb9c6fe47d&dn=www.5MovieRulz.loan%20-%20Radhaa%20Madhavam%20(2024)%20Telugu%20HQ%20HDRip%20-%20x264%20-%20AAC%20-%20400MB%20-%20ESub.mkv&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2ftracker.torrent.eu.org%3a451%2fannounce&tr=udp%3a%2f%2ftracker.dler.org%3a6969%2fannounce&tr=udp%3a%2f%2fopen.stealth.si%3a80%2fannounce&tr=udp%3a%2f%2fopentracker.i2p.rocks%3a6969%2fannounce&tr=udp%3a%2f%2ftracker-udp.gbitt.info%3a80%2fannounce&tr=udp%3a%2f%2ftracker.tiny-vps.com%3a6969%2fannounce&tr=udp%3a%2f%2fmovies.zsw.ca%3a6969%2fannounce&tr=https%3a%2f%2fopentracker.i2p.rocks%3a443%2fannounce"
req=requests.get(f"https://api.streamwish.com/api/upload/magnet?key={key}&url={quote(url)}")
print(req.json())