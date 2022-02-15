from unicodedata import name
from django.urls import path
from .views import article_list
from . import views

urlpatterns=[
    path('article/',article_list,),
    path('article/<int:pk>',views.article_detail,name='article_detail'),
]