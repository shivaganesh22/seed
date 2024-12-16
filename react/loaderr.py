from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests

domain="https://p.oceansaver.in/"
api="dfcb6d76f2f6a9894gjkege8a4ab232222"

@api_view(["GET"])
def youtube(r):
    quality=r.GET["quality"]
    url=r.GET["url"]
    res=requests.get(f"{domain}ajax/download.php?format={quality}&url={url}&api={api}")
    return Response(res.json(),status=status.HTTP_200_OK)
@api_view(["GET"])
def youtube_progress(r):
    id=r.GET["id"]
    res=requests.get(f"{domain}ajax/progress.php?id={id}")
    return Response(res.json(),status=status.HTTP_200_OK)
