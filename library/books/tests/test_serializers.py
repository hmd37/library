from django.test import TestCase
from django.utils.text import slugify

from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            description="A great book about testing."
        )

    def test_serializer_valid_data(self):
        """Test if serializer is valid with correct data"""
        data = {
            "title": "Another Book",
            "author": "Jane Doe",
            "description": "A new book."
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serialized_output(self):
        """Test serializer output for an existing book instance"""
        serializer = BookSerializer(instance=self.book)
        expected_data = {
            "id": self.book.id,
            "title": "Test Book",
            "author": "John Doe",
            "description": "A great book about testing.",
            "published_date": str(self.book.published_date),  
            "slug": slugify(f"Test Book John Doe")  
        }
        self.assertEqual(serializer.data, expected_data)
