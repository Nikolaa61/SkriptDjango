from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
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

    for article1 in tmp:
        zbir = 0
        brOcena = 0

        if tmp2 is not None:
            for ocena in tmp2:
                if ocena.article == article1:
                    zbir = zbir + ocena.broj
                    brOcena = brOcena + 1
            prosek = 0
            if brOcena != 0:
                prosek = zbir / brOcena
            article1.prosecnaOcena = prosek
    return render(req, 'articles.html', {'articles': tmp})


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

@login_required
def oceni(req, id):
    if req.method == 'POST':
        form = OcenaForm(req.POST)

        if form.is_valid():
            o = Ocena(broj=form.cleaned_data['broj'], content=form.cleaned_data['content'])
            a = Article.objects.get(id=id)
            o.article = a
            o.owner = sample_view(req)
            o.save()
            return redirect('ocenjivanje:articles')
        else:
            return render(req, 'oceni.html', {'form': form, 'id': id})
    else:
        form = OcenaForm()
        return render(req, 'oceni.html', {'form': form, 'id': id})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('ocenjivanje:articles')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def promeniOcenu(req, id):
    if req.method == 'POST':
        form = OcenaForm(req.POST)
        user = sample_view(req)
        if form.is_valid():
            o = Ocena(broj=form.cleaned_data['broj'], content=form.cleaned_data['content'])
            a = Article.objects.get(id=id)
            o.article = a
            o.owner = user
            if form.is_valid():
                tmp2 = Ocena.objects.all()
                if tmp2 is not None:
                    for ocena in tmp2:
                        if ocena.article == a:
                            if ocena.owner == user:
                                ocena.broj = o.broj
                                ocena.content = o.content
                                ocena.save()
            return redirect('ocenjivanje:articles')
        else:
            return render(req, 'editOcena.html', {'form': form, 'id': id})
    else:
        form = OcenaForm()
        return render(req, 'editOcena.html', {'form': form, 'id': id})


def sample_view(request):
    return request.user
