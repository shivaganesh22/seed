from django.db import models

# Create your models here.
class StreamLink(models.Model):
    slug=models.CharField(max_length=500,unique=True)
    def __str__(self):
        return self.slug
class EachStream(models.Model):
    movie=models.ForeignKey(StreamLink,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    account=models.IntegerField()
    link=models.CharField(max_length=1500)
    is_uploaded=models.BooleanField(default=False)
    is_edited=models.BooleanField(default=False)
    count=models.IntegerField(default=0,null=True)
    def __str__(self):
        return self.name+" "+self.movie.slug
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string


class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auth_tokens")
    key = models.CharField(max_length=40, unique=True)
    device_info = models.TextField(blank=True, null=True)
    browser_info = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_used = models.DateTimeField(default=timezone.now)
    expiry = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    DEFAULT_EXPIRY_DAYS = 7

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get_random_string(40)
        if not self.expiry:
            self.expiry = timezone.now() + timezone.timedelta(days=self.DEFAULT_EXPIRY_DAYS)
        super().save(*args, **kwargs)

    def is_valid(self):
        if not self.is_active:
            return "Session has been blocked by admin",False
        if not self.user.is_active:
            return "User has been blocked by admin",False
        if self.expiry and timezone.now() > self.expiry:
            return "Your session has expired due to inactivity.",True
        return 'success',False
    def extend_expiry(self):
        """Extend expiry by 7 days from now (rolling expiration)."""
        self.expiry = timezone.now() + timezone.timedelta(days=self.DEFAULT_EXPIRY_DAYS)
        self.save(update_fields=["expiry"])
    def __str__(self):
        return self.user.email +" "+ str(self.created) + " "+self.browser_info
class LockFolder(models.Model):
    folder_id=models.CharField(max_length=30,unique=True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.folder_id + "   " + str (self.created)