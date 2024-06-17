from django.test import TestCase

# Create your tests here.
import requests
key="56925fxislvf4q1zn2qfp"

import time
from urllib.parse import quote
from seedrcc import Login,Seedr
seedr=Login("shivaganeshrsg1@gmail.com","Shiva123@")
response=seedr.authorize()
ac=Seedr(seedr.token)
data=ac.listContents()
# print(data)
for i in range(1):
    # time.sleep(20)
    if data["folders"]:
        folder=ac.listContents(folderId=data["folders"][-1]["id"])
        if folder["files"]:
            file=ac.fetchFile(fileId=folder["files"][-1]["folder_file_id"])
            url=quote(file["url"])
            req=requests.get(f"https://filemoonapi.com/api/remote/add?key={key}&url={url}")
            print(req)
# if data["torrents"]:
#     ac.deleteTorrent(torrentId=data["torrents"][-1]["id"])
