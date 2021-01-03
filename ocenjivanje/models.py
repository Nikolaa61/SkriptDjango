from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.TextField(default="")
    content = models.TextField(default="")
    prosecnaOcena = models.FloatField(default=0)

    def __str__(self):
        return self.title + ' ' + self.prosecnaOcena

class Ocena(models.Model):
    content = models.CharField(max_length=256)
    broj = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.contentt + ' ' + self.broj
