# app

from django.urls import path
from .views import BookList, BookDetail


urlpatterns = [
    path('books/',BookList.as_view(), name='book_list'),
    path('books/<int:pk>/',BookDetail.as_view(),name='book_detail'),

]