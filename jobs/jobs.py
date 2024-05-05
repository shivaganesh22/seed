import requests
import json
from app.models import *
def send_fcm_notification( title, body,image,link):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAhHqY1L0:APA91bF76GAl0BG_JOc9UNOTmQCBAA8irf_7z9zRRIr7NmvM3Gr4VYYTnHAMLb-ZP-td473Bfjek76dYR81a0xnRRFkPihOeTdA8quIotP8uw685M6ZjZJrL-jokGGreuRywtYd7JdJj',  # Replace YOUR_SERVER_KEY with your Firebase Server key
    }
    payload = {
        'to': '/topics/movies',
        'data': {  # Use 'data' instead of 'notification'    
            'link': link,
        },
        'notification': {
            'title': title,
            'body': body,
            'image':image,
        },
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(body)
    else:
        print("Failed to send notification:", response.text)

def movierulz_fcm():
    response=requests.get("https://rsg-movies.vercel.app/react/movierulz/")
    try:
        data=response.json()
        new_movies=[]
        for i in data['movies']:
            new_movies.append(Movierulz(name=i['name'],image=i['image'],link=i['link']))
            if not Movierulz.objects.filter(name=i['name']).exists():
                send_fcm_notification("Movierulz Movie Update",i['name'],i['image'],'/movierulz/movie?link='+i['link'])
        Movierulz.objects.all().delete()
        print("movierulz deleted")
        Movierulz.objects.bulk_create(new_movies)
        print("movierulz added")
    except :
        pass
def ibomma_fcm():
    response=requests.get("https://rsg-movies.vercel.app/api/ibomma/")
    try:
        data=response.json()
        new_movies=[]
        for i in data['movies']:
            new_movies.append(IBomma(name=i['name'],image=i['image'],link=i['link']))
            if not IBomma.objects.filter(name=i['name']).exists():
                send_fcm_notification("IBomma Movie Update",i['name'],i['image'],'/ibomma/movie?link='+i['link'])
        IBomma.objects.all().delete()
        print("ibomma deleted")
        IBomma.objects.bulk_create(new_movies)
        print("ibomma added")
  
    except :
        pass

    

