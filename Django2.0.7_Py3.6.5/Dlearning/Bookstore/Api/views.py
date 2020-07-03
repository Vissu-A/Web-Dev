from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.parsers import JSONParser

from Bookstore.models import Book, Author, Publisher
from Bookstore.Api.serializers import Bookserializer, Authorserializer, Publisherserializer

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def allbooks(request):
    queryset = Book.objects.all()
    print(queryset)
    
    if request.method == 'GET':
        seril = Bookserializer(queryset, many=True)
        return Response(seril.data)


class allbooksapiview(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = Bookserializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated,]
    # pagination_class = settings.DEFAULT_PAGINATION_CLASS
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'price', 'rating', 'author__name', 'publisher__name']
    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def allauthors(request):
    
    print(request.user.is_superuser)
    
    queryset = Author.objects.all()
    
    print(queryset)
    
    if request.method == 'GET':
        paginator = Paginator(queryset, 3)
        page = request.GET.get('page')
    
        try:
            authorlist = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            authorlist = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            authorlist = paginator.page(paginator.num_pages)
            
        seril = Authorserializer(authorlist, many=True)
        return Response(seril.data)
    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def allpublishers(request):
    
    queryset = Publisher.objects.all()
    print(queryset)
    
    if request.method == 'GET':
        seril = Publisherserializer(queryset, many=True)
        return Response(seril.data)
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateauthor(request, authname):
    
    if not request.user.is_superuser:
        return Response({"error":"You don't have permission to update."}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        auth = Author.objects.get(name=authname)
    except Author.DoesNotExist:
        return Response('No author exists with the name '+authname, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = Authorserializer(auth, data=request.data, partial=True)   # Keeps partial = True if you dont want to pass values for all variabiles in the model, otherwise it will raise Field required error.
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update success...'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createbook(request):

    if not request.user.is_superuser:
        return Response({"error":"You don't have permission to add."}, status=status.HTTP_403_FORBIDDEN)
    
    auth = Author.objects.get(pk=1)
    pub = Publisher.objects.get(pk=1)
    
    book = Book(author=auth, publisher=pub)
  
    if request.method == 'POST':
        serializer = Bookserializer(book, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update success...'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deletebook(request, bookname):

    if not request.user.is_superuser:
        return Response({"error":"You don't have permission to delete."}, status=status.HTTP_403_FORBIDDEN)
       
    try:
        book = Book.objects.get(name=bookname)
    except Book.DoesNotExist:
        return Response('No book with the name '+bookname, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'DELETE':
        deleted = book.delete()
        data = {}
        if deleted:
            data['success'] = 'Delete success...'
        else:
            data['failure'] = 'Delete failed!'
        
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          