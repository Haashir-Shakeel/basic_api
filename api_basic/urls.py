from django.urls import path, include
from .views import AricleDetailApiView, ArticleDetailGeneric, ArticleDetailMixin, ArticleListApiView, ArticleListGeneric, ArticleListMixin, article_list, ArticleViewSet, ArticleGenericViewSet, ArticleModelViewSet
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')
router.register('genarticle',ArticleGenericViewSet,basename='genarticle')
router.register('modarticle',ArticleModelViewSet,basename='modarticle')


urlpatterns=[
    # path('viewset/', include(router.urls)),
    path('article/',article_list,),
    path('article/<int:pk>',views.article_detail,name='article_detail'),
    path('classarticle/',ArticleListApiView.as_view(),name='class_article_list'),
    path('classarticle/<int:pk>',AricleDetailApiView.as_view(),name='class_article_detail'),
    path('mixinarticle/',ArticleListMixin.as_view(),name='mixin_article_list'),
    path('mixinarticle/<int:pk>',ArticleDetailMixin.as_view(),name='mixin_article_detail'),
    path('genericarticle/',ArticleListGeneric.as_view(),name='generic_article_list'),
    path('genericarticle/<int:pk>',ArticleDetailGeneric.as_view(),name='generic_article_detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns.append(path(r'viewset/', include(router.urls)))
urlpatterns.append(path(r'viewset/<int:pk>/', include(router.urls)))
urlpatterns.append(path(r'genericviewset/', include(router.urls)))
urlpatterns.append(path(r'genericviewset/<int:pk>/', include(router.urls)))
urlpatterns.append(path(r'modelviewset/', include(router.urls)))
urlpatterns.append(path(r'modelviewset/<int:pk>/', include(router.urls)))