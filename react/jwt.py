from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.utils import timezone
from user_agents import parse
from .models import *
from .serializers import *
from seedrcc import Login,Seedr
from django.contrib.auth.models import User
from .utils import DeviceInfoManager
from .authentication import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
import requests
class JWTLoginApi(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                seedr = Login(email, password)
                response = seedr.authorize()
                Seedr(token=seedr.token)
                
                # Get or create user
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': f"{email}_{password}",
                        'password': password
                    }
                )
                if not user.is_active:
                    return Response({'error': "User has been blocked by admin"},status=status.HTTP_400_BAD_REQUEST)
                
                device_info, browser_info, user_agent = DeviceInfoManager.get_device_info(request)
                ip_address = DeviceInfoManager.get_client_ip(request)
                location = DeviceInfoManager.get_location_from_ip(ip_address)
                
                # Create session with refresh token JTI
                session = UserToken.objects.create(
                    user=user,
                    device_info=device_info,
                    browser_info=browser_info,
                    ip_address=ip_address,
                    location=location,
                    user_agent=user_agent,
                    page="login"
                )
                
                return Response({
                    "session":session.key,
                    "rsg":user.is_superuser
                })
                
            except Exception as e:
                return Response({'error': "Invalid Credentials"}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class JWTDefaultLogin(APIView):
    def get(self,request):
        user=User.objects.get(id=4)
        if not user.is_active:
            return Response({'error': "User has been blocked by admin"},status=status.HTTP_400_BAD_REQUEST)
        device_info, browser_info, user_agent = DeviceInfoManager.get_device_info(request)
        ip_address = DeviceInfoManager.get_client_ip(request)
        location = DeviceInfoManager.get_location_from_ip(ip_address)
        
        # Create session with refresh token JTI
        session = UserToken.objects.create(
            user=user,
            device_info=device_info,
            browser_info=browser_info,
            ip_address=ip_address,
            location=location,
            user_agent=user_agent,
        )
        
        return Response({
            "session":session.key,
            "rsg":user.is_superuser
        })
class JWTCodeLogin(APIView):
    def get(self,request,code):
        if code=="rsg":
            user=User.objects.get(id=3)
        elif code=="gani":
            user=User.objects.get(id=2)
        else:
            return Response({'error': "Invalid Code"},status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'error': "User has been blocked by admin"},status=status.HTTP_400_BAD_REQUEST)
        device_info, browser_info, user_agent = DeviceInfoManager.get_device_info(request)
        ip_address = DeviceInfoManager.get_client_ip(request)
        location = DeviceInfoManager.get_location_from_ip(ip_address)
        
        # Create session with refresh token JTI
        session = UserToken.objects.create(
            user=user,
            device_info=device_info,
            browser_info=browser_info,
            ip_address=ip_address,
            location=location,
            user_agent=user_agent,
        )
        
        return Response({
            "session":session.key,
            "rsg":user.is_superuser
        })
class JWTLogoutApi(APIView):
    def post(self, request):
        token_key = request.data.get("token")
        if not token_key:
            return Response({ "error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = UserToken.objects.get(key=token_key)
        except UserToken.DoesNotExist:
            return Response({"message": "Already logged out"}, status=status.HTTP_200_OK)
        token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

def getSeedr(r):
    seedr=Login(r.user.email,r.user.password)
    response=seedr.authorize()
    try:
        ac=Seedr(seedr.token)
        return ac
    except:
        return None
def getCookie(r):
    try:
        ress=requests.post('https://www.seedr.cc/auth/login', data={'username':r.user.email,"password":r.user.password})
        cookies=requests.utils.dict_from_cookiejar(ress.cookies)
        return cookies
    except:
        return None
    
class JWTFilesApi(APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r):
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        try:
            data=ac.listContents(id)
            data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
            data["files"] = sorted(data['files'], key=lambda x: x['name'])
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({ "detail":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
    
class JWTOpenFolder( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        try:
            data=ac.listContents(id)
            data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"],reverse=True)
            data["files"] = sorted(data['files'], key=lambda x: x['name'])
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({ "detail":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
class JWTFolderFile( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        try:
            files=ac.listContents(id)['files']
            data=ac.fetchFile(files[0]['folder_file_id'])
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({ "detail":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
        
class JWTFolderArchieve( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getCookie(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        try:
            res=requests.post("https://www.seedr.cc/download/archive",cookies=ac,data={"archive_arr[0][type]": "folder","archive_arr[0][id]":id})
            data=res.json()
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({ "detail":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
        

class JWTFolderFilePlayer( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        data={}
        files={}    
        try:
            files=ac.listContents(id)['files']
            data=ac.fetchFile(files[0]['folder_file_id'])
        except:
            return Response({ "detail":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
        try:
            cookies=getCookie(r)
            res=requests.get(f"https://www.seedr.cc/presentation/fs/item/{files[0]['folder_file_id']}/video/url",cookies=cookies)
            data["m3u8"]=res.json()["url"]
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response(data,status=status.HTTP_200_OK)

class JWTGetFile( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)           
        try:
            return Response(ac.fetchFile(id),status=status.HTTP_200_OK)
        except:
            return Response({ "detail":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
class JWTGetFilePlayer( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST) 
        data={}
        try:
            data=ac.fetchFile(id)
        except:
            return Response({ "detail":"Falied to get results"},status=status.HTTP_400_BAD_REQUEST)
        try:
            cookies=getCookie(r)
            res=requests.get(f"https://www.seedr.cc/presentation/fs/item/{id}/video/url",cookies=cookies)
            data["m3u8"]=res.json()["url"]
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response(data,status=status.HTTP_200_OK)


class JWTAddTorrent( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        link=r.GET.get('link')
        res=ac.addTorrent(link)
        return Response(res,status=status.HTTP_200_OK)
class JWTDeleteTorrent( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        res=ac.deleteTorrent(id)
        return Response(res,status=status.HTTP_200_OK)
    
class JWTDeleteFolder( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        if LockFolder.objects.filter(folder_id=id).exists():
            return  Response({ "detail":"Folder locked by admin"},status=status.HTTP_400_BAD_REQUEST)
        res=ac.deleteFolder(id)
        return Response(res,status=status.HTTP_200_OK)
    
class JWTDeleteFile( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id,fid):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        if LockFolder.objects.filter(folder_id=fid).exists():
            return  Response({ "detail":"Folder locked by admin"},status=status.HTTP_400_BAD_REQUEST)
        res=ac.deleteFile(id)
        return Response(res,status=status.HTTP_200_OK)
    
class JWTRenameFolder( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        name=r.GET['name']
        res=ac.renameFolder(id,name)
        if res['result']:
            return Response(res,status=status.HTTP_200_OK)
        else:
            return Response({ "detail":res['error'].title()},status=status.HTTP_401_UNAUTHORIZED)
    
class JWTRenameFile( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        name=r.GET['name']
        res=ac.renameFile(id,name)
        if res['result']:
            return Response(res,status=status.HTTP_200_OK)
        else:
            return Response({ "detail":res['error'].title()},status=status.HTTP_401_UNAUTHORIZED)
    
class JWTLockFolder( APIView):
    authentication_classes=[CustomTokenAuthentication]
    def get(self,r,id):  
        ac=getSeedr(r)
        if not ac:
            return  Response({ "detail":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        if r.user.is_superuser:
            try:
                LockFolder.objects.create(folder_id=id)
                return Response({"detail":"Locked Folder"})
            except:
                LockFolder.objects.get(folder_id=id).delete()
                return  Response({ "detail":"Unlocked Folder"})
        else:
            return  Response({ "detail":"You dont have permission"},status=status.HTTP_400_BAD_REQUEST)

class JWTShareFolder(APIView):
    authentication_classes = [CustomTokenAuthentication]
    def get(self, request, id):  
        try:
            session = request.auth  
            share, created = ShareFolder.objects.get_or_create(
                folder_id=id,
                session=session,
                defaults={
                    "name": request.GET.get("name")
                }
            )
            return Response({ "name": share.name,"link": f"https://rsgmovies.vercel.app/share/{share.link}","already_shared": not created }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Failed to create link"},status=status.HTTP_400_BAD_REQUEST)
def getShareLogin(session):
    seedr=Login(session.user.email,session.user.password)
    response=seedr.authorize()
    try:
        ac=Seedr(seedr.token)
        return ac
    except:
        return None

class JWTGetShareFolder(APIView):
    def get(self, request,link):
        # Collect device/browser info
        device_info, browser_info, user_agent = DeviceInfoManager.get_device_info(request)
        ip_address = DeviceInfoManager.get_client_ip(request)
        location = DeviceInfoManager.get_location_from_ip(ip_address)

        try:
            share = ShareFolder.objects.get(link=link)

            # Authenticate with Seedr using session
            ac = getShareLogin(share.session)
            if not ac:
                return Response({"detail": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch folder contents
            data = ac.listContents(share.folder_id)
            # data["folders"] = sorted(data["folders"], key=lambda x: x["last_update"], reverse=True)
            data["files"] = sorted(data['files'], key=lambda x: x['name'])

            k=AccessFolder.objects.create(
                share=share,
                device_info=device_info,
                browser_info=browser_info,
                ip_address=ip_address,
                location=location,
                user_agent=user_agent,
                page="open folder"
            )
            data["key"]=k.link
            data["link"]=f"https://rsgmovies.vercel.app/share/{link}"
            
            return Response(data, status=status.HTTP_200_OK)

        except ShareFolder.DoesNotExist:
            return Response({"detail": "Invalid Share Link"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Failed to get results"}, status=status.HTTP_400_BAD_REQUEST)

class JWTFetchShareFolder(APIView):
    def get(self, request, id,link):
        try:
            access = AccessFolder.objects.get(link=link)
            ac = getShareLogin(access.share.session)
            if not ac:
                return Response({"detail": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the file from Seedr
            file_obj = ac.fetchFile(id)

            # Collect updated request metadata
            ip_address = DeviceInfoManager.get_client_ip(request)
            location = DeviceInfoManager.get_location_from_ip(ip_address)

            # Update access record
            access.ip_address = ip_address
            access.location = location
            access.page = f"access file {file_obj.get('name', id)}"
            access.last_used = timezone.now()
            access.save(update_fields=["ip_address", "location", "page", "last_used"])

            return Response(file_obj, status=status.HTTP_200_OK)

        except AccessFolder.DoesNotExist:
            return Response({"detail": "Invalid Share Link"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Failed to get results"}, status=status.HTTP_400_BAD_REQUEST)