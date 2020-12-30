from django.forms import ModelForm
from .models import Article, Ocena

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        field = ['title']

class OcenaForm(ModelForm):
    class Meta:
        model = Ocena
        field = ['broj', 'content']