from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.utils import timezone
from .models import UserToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .utils import DeviceInfoManager
class CustomTokenAuthentication(BaseAuthentication):
    keyword = "Token"

    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith(self.keyword):
            return None

        token_key = auth.split()[1]
        try:
            token = UserToken.objects.get(key=token_key)
        except UserToken.DoesNotExist:
            raise AuthenticationFailed("Session not found. Please try logging in again")

        msg, action = token.is_valid()
        if msg != 'success':
            raise AuthenticationFailed(f"{msg}")

        # Update last used, IP, location, page
        ip_address = DeviceInfoManager.get_client_ip(request)
        location = DeviceInfoManager.get_location_from_ip(ip_address)

        token.last_used = timezone.now()
        token.ip_address = ip_address
        token.location = location
        token.page = request.path  # store the API endpoint being accessed

        # Extend expiry (sliding 7 days)
        token.extend_expiry()

        token.save(update_fields=["last_used", "ip_address", "location", "page"])
        return (token.user, token)