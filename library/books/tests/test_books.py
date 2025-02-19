from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book 
from books.serializers import BookSerializer 


class BookAPITestCase(APITestCase):
    def setUp(self):
        """
        Create test books for use in test cases.
        """
        self.book1 = Book.objects.create(
            title="Book One", author="Author A", description="First book",
            slug="book-one-author-a", published_date="2023-01-01"
        )
        self.book2 = Book.objects.create(
            title="Book Two", author="Author B", description="Second book",
            slug="book-two-author-b", published_date="2024-01-01"
        )

    def test_book_list_api(self):
        """
        Test retrieving a list of books.
        """
        url = reverse("book-list")
        response = self.client.get(url)

        books = Book.objects.all().order_by("published_date")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)  

    def test_book_list_ordering(self):
        """
        Test ordering of books by title.
        """
        url = reverse("book-list") + "?ordering=title"
        response = self.client.get(url)

        books = Book.objects.all().order_by("title")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_book_detail_by_id(self):
        """
        Test retrieving a book by its ID.
        """
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)

        serializer = BookSerializer(self.book1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_detail_by_slug(self):
        """
        Test retrieving a book by its slug.
        """
        url = reverse("book-detail", args=[self.book1.slug]) 
        response = self.client.get(url)

        serializer = BookSerializer(self.book1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_detail_not_found(self):
        """
        Test retrieving a book that does not exist.
        """
        url = reverse("book-detail", args=["nonexistent"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_book_auto_slug_generation(self):
        """
        Test slug generation when saving a book without a slug.
        """
        book = Book.objects.create(
            title="New Book", author="Author X", description="Test book"
        )
        expected_slug = slugify(f"{book.title} {book.author}")

        self.assertEqual(book.slug, expected_slug)
