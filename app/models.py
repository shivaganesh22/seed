from django.db import models

# Create your models here.
class Contact(models.Model):
    full_name=models.CharField(max_length=20)
    email=models.EmailField()
    subject=models.CharField(max_length=6)
    message=models.TextField()
    def __str__(self):
        return self.full_name+" "+self.subject