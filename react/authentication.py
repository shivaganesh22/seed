from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.utils import timezone
from .models import UserToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
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
            raise AuthenticationFailed("Session not found")
        msg,action=token.is_valid()
        if msg!='success':
            raise AuthenticationFailed(f"{msg}")

        # Update last used
        token.last_used = timezone.now()

        # Extend expiry (sliding 7 days)
        token.extend_expiry()

        token.save(update_fields=["last_used"])
        return (token.user, token)