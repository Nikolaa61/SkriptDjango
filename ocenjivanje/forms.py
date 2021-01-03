from django.forms import ModelForm
from .models import Article, Ocena

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class OcenaForm(ModelForm):
    class Meta:
        model = Ocena
        fields = ['broj', 'content']