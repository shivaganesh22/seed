from django.db import models

# Create your models here.
class StreamLink(models.Model):
    slug=models.CharField(max_length=500,unique=True)
    status=models.BooleanField(default=True)
    def __str__(self):
        return self.slug
class EachStream(models.Model):
    movie=models.ForeignKey(StreamLink,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    account=models.IntegerField()
    link=models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.name+" "+self.movie.slug