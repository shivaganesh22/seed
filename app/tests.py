from django.test import TestCase

# Create your tests here.
import requests
# auth_token="o+FReHCGQi8VUIYRGZ8Mqyn5lAsRWTiQY8LujIZCYkk="
auth_token="k1nkbA6NJbsR+lq2HidFz7y670h4f1wCBLWDWjJuiiM="
import requests
import json
import time

# Define the URL and the authorization token
url = "https://api.cron-job.org/jobs"
response = requests.get(
        url,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
        
    )
job_data = {
        "job": {
            "enabled": True
        }
    }

if response.status_code==200:
    for i in response.json()["jobs"]:
        res = requests.patch(
        url+"/"+i["jobId"],
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        },
        data=json.dumps(job_data)
    )
        time.sleep(2)
        if res.status_code==200:
            print("updated",i["jobId"])
        else:
            print("Failed",i["jobId"])
else:
    print("sss")
# Define the job data


job_data1 = {
        "job": {
            "url": "https://rsg-movies.vercel.app/react/task4/",
            "enabled": False,
            "title":"task 4",
            "saveResponses": True,
            "schedule": {
                "timezone": "Europe/Berlin",
                "expiresAt": 0,
                "hours": [20],    # 0 for 12 AM
                "mdays": [-1],   # Every day
                "minutes": [0],  # 5 minutes past the hour
                "months": [-1],  # Every month
                "wdays": [-1]    # Every weekday
            }
        }
    }



# Check the response
