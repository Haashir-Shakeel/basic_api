#https://www.youtube.com/watch?v=B38aDwUpcFc

from ast import Pass
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from api_basic.models import Article
from api_basic.serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        # print("#1")
        # print(articles)
        serializer = ArticleSerializer(articles, many=True)
        # print("#2")
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)



@csrf_exempt
def article_detail(request,pk):
    
    try:
        article = Article.objects.get(id=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        Pass

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)
