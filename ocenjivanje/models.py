from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.TextField()
    prosecnaOcena = models.FloatField(default=0)

    def __str__(self):
        return self.title + ' ' + self.prosecnaOcena

class Ocena(models.Model):
    contentt = models.CharField(max_length=256)
    broj = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.contentt + ' ' + self.broj
