from django.http import Http404
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import status
# from django.http import HttpResponse,JsonResponse
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from api_basic import serializers
from api_basic.models import Article
from api_basic.serializers import ArticleSerializer
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404





#***************** VIEWSETS *********************

# ModelViewSet
class ArticleModelViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes=[TokenAuthentication]

# GenericViewSet

class ArticleGenericViewSet(viewsets.GenericViewSet,ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# ViewSet
class ArticleViewSet(viewsets.ViewSet):

    def list(self, request,format=None):
        articles=Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)
    

    def create(self,request,format=None):
        serializer=ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None,format=None):
        queryset=Article.objects.all()
        article = get_object_or_404(queryset,id=pk)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)

    def update(self,request,pk=None,format=None):
        article=Article.objects.get(id=pk)
        serializer=ArticleSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None,fromat=None):
        article=Article.objects.get(id=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









# **************** USING GENERIC CLASS BASED VIEWS ***************** 

class ArticleListGeneric(ListCreateAPIView):
    queryset=Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  

class ArticleDetailGeneric(RetrieveUpdateDestroyAPIView):
    queryset=Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

# **************** USING MIXIN CLASS BASED VIEWS ******************



class ArticleListMixin(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes=[SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args,**kwargs):
        return self.list(request, *args,**kwargs)

    def post(self, request, *args,**kwargs):
        return self.create(request, *args,**kwargs)

class ArticleDetailMixin(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Article.objects.all()
    serializer_class= ArticleSerializer
    authentication_classes=[SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self, request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self, request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

# ************* CLASS BASED API VIEWS *********************
class ArticleListApiView(APIView):
    authentication_classes=[SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,format=None):
        articles = Article.objects.all()
        serializer= ArticleSerializer(articles, many = True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AricleDetailApiView(APIView):
    authentication_classes=[SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Article.objects.get(id=pk)
        except Article.DoesNotExist:
            raise Http404


    def get(self,request, pk,format=None):
        article=self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        article=self.get_object(pk)
        serializer=ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk,format=None):
        article=self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    



# ***************   FUNCTION BASED API VIEWS **********************

@api_view(['GET','POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def article_list(request, format=None):
    if request.method == 'GET':
        articles = Article.objects.all()
        # print("#1")
        # print(articles)
        serializer = ArticleSerializer(articles, many=True)
        # print("#2")
        # print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk, format = None):
    
    try:
        article = Article.objects.get(id=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
