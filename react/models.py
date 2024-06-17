from django.db import models

# Create your models here.
class StreamLink(models.Model):
    slug=models.CharField(max_length=1000,unique=True)
    link=models.CharField(max_length=500)
    def __str__(self):
        return self.link +" "+self.slug