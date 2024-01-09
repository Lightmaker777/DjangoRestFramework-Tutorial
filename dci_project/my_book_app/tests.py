from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date,timedelta
from django.utils.text import slugify
from .models import Book
from .serializers import BookSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BookTests(APITestCase):
    
    
    def setUp(self) :
        
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin','admin@test.py','testpassword'
        )
        self.token = Token.objects.create(user = self.admin_user)
        self.user = User.objects.create_user("user", "admin@test.com", "testpassword")
        self.user_token = Token.objects.create(user=self.user)
        self.book = Book.objects.create(
            title="The Alchemist",
            author="Paulo Coelho",
            description="A book about following your dreams",
            published_date=date.today() - timedelta(days=7),
            is_published=False,
        )
        self.valid_payload = {
            "title": "The Alchemist 1",
            "author": "Paulo Coelho",
            "description": "A book about following your dreams",
            "published_date": date.today() - timedelta(days=7),
            "is_published": False,
        }
        self.invalid_payload = {
            "title": "",
            "author": "",
            "description": "",
            "published_date": date.today() + timedelta(days=7),
            "is_published": False,
        }
        
    def test_get_all_books(self):
        response = self.client.get(reverse('book_list'))
        books = Book.objects.all()
        serializer = BookSerializer(books,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_get_single_book(self):
        
        response = self.client.get(reverse('book_detail',args=[self.book.id]))
        book = Book.objects.get(id=self.book.id)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_valid_book(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            reverse("book_list"), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_book_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        url = reverse("book_list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "description": "New Description",
            "published_date": "2021-01-01",
            "is_published": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_authentication_required_for_post_book(self):
        url = reverse('book_list')
        response = self.client.post(url,data=self.valid_payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_create_invalid_book(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(reverse('book_list'),data=self.invalid_payload,format='json')        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_book(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)      
        updated_payload = self.valid_payload.copy()
        updated_payload['title'] = "The Alchemist Revised"
        response = self.client.put(
            reverse('book_detail',args=[self.book.id]),
            data=updated_payload,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(slugify(response.data['title']),slugify(updated_payload["title"]))
        
    def test_delete_book(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(reverse("book_detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        