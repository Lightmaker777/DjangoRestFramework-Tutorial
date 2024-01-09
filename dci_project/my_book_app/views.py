from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
# Create your views here.


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        try :
            serializer.save()           
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
            
    
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
        
    def perform_destroy(self, instance):
        instance.delete()





