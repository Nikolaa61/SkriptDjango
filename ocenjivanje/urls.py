
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='ocenjivanje_index'),
    path('hello/', views.hello, name='ocenjivanje_hello'),
]
