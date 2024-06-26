from django.db import models

# Create your models here.
class Contact(models.Model):
    full_name=models.CharField(max_length=20)
    email=models.EmailField()
    subject=models.CharField(max_length=6)
    message=models.TextField()
    def __str__(self):
        return self.full_name+" "+self.subject
class Movierulz(models.Model):
    name=models.CharField(max_length=150)
    image=models.URLField()
    link=models.URLField()
    def __str__(self):
        return self.name
class IBomma(models.Model):
    name=models.CharField(max_length=150)
    image=models.URLField()
    link=models.URLField()
    def __str__(self):
        return self.name
class FCM_token(models.Model):
    token=models.CharField(max_length=500,unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
