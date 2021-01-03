from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Article, Ocena
from .forms import ArticleForm, OcenaForm


def index(req):
    if not req.user.is_authenticated:
        return render(req, 'index.html', {'page_title': 'Vezbe 13'})
    else:
        return redirect('ocenjivanje:articles')


@login_required
def articles(req):
    tmp = Article.objects.all()
    tmp2 = Ocena.objects.all()
    return render(req, 'articles.html', {'articles': tmp, 'ocene':tmp2})


@login_required
def article(req, id):
    tmp = get_object_or_404(Article, id=id)
    return render(req, 'article.html', {'article': tmp, 'page_title': tmp.title})


@permission_required('ocenjivanje.change_article')
def edit(req, id):
    if req.method == 'POST': # moze da bude post kad se klikne save u edit.htm ili da ne bude nego samo kad se klikne edit da renderuje edit.html
        form = ArticleForm(req.POST)

        if form.is_valid():
            a = Article.objects.get(id=id)
            a.title = form.cleaned_data['title']
            a.content = form.cleaned_data['content']
            a.save()
            return redirect('ocenjivanje:articles')
        else:
            return render(req, 'edit.html', {'form': form, 'id': id})
    else:
        a = Article.objects.get(id=id)
        form = ArticleForm(instance=a)
        return render(req, 'edit.html', {'form': form, 'id': id})

@permission_required('ocenjivanje.add_article')
def new(req):
    if req.method == 'POST':
        form = ArticleForm(req.POST)

        if form.is_valid():
            a = Article(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            a.save()
            return redirect('ocenjivanje:articles')
        else:
            return render(req, 'new.html', {'form': form})
    else:
        form = ArticleForm()
        return render(req, 'new.html', {'form': form})

@login_required('ocenjivanje.oceni_artikal')
def oceni(req, id):
    if req.method == 'POST':
        form = OcenaForm(req.POST)

        if form.is_valid():
            o = Ocena(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            o.save()
            return redirect('ocenjivanje:articles')
        else:
            return render(req, 'oceni.html', {'form': form})
    else:
        form = ArticleForm()
        return render(req, 'oceni.html', {'form': form})