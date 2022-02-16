from unicodedata import name
from django.urls import path
from .views import AricleDetailApiView, ArticleDetailMixin, ArticleListApiView, ArticleListMixin, article_list
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
    path('article/',article_list,),
    path('article/<int:pk>',views.article_detail,name='article_detail'),
    path('classarticle/',ArticleListApiView.as_view(),name='class_article_list'),
    path('classarticle/<int:pk>',AricleDetailApiView.as_view(),name='class_article_detail'),
    path('mixinarticle/',ArticleListMixin.as_view(),),
    path('mixinarticle/<int:pk>',ArticleDetailMixin.as_view(),name='mixin_article_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)