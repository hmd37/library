from django.test import TestCase
from django.utils.text import slugify

from books.models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Django Testing",
            author="John Doe",
            description="A book about testing Django applications."
        )

    def test_book_creation(self):
        """Test if a Book instance is created correctly"""
        self.assertEqual(self.book.title, "Django Testing")
        self.assertEqual(self.book.author, "John Doe")
        self.assertEqual(self.book.description, "A book about testing Django applications.")

    def test_slug_generation(self):
        """Test if slug is auto-generated correctly"""
        expected_slug = slugify(f"{self.book.title} {self.book.author}")
        self.assertEqual(self.book.slug, expected_slug)

    def test_slug_preservation(self):
        """Test if an existing slug is not overwritten when updating the book"""
        custom_slug = "custom-slug"
        book = Book.objects.create(title="New Book", author="Jane Doe", slug=custom_slug)
        book.title = "Updated Book"
        book.save()
        self.assertEqual(book.slug, custom_slug)

    def test_blank_title_and_author(self):
        """Test if a book can be created with blank title and author"""
        book = Book.objects.create(description="No title or author")
        self.assertIsNone(book.title)
        self.assertIsNone(book.author)
        self.assertEqual(book.description, "No title or author")

    def test_string_representation(self):
        """Test the __str__ method of the Book model"""
        self.assertEqual(str(self.book), "Django Testing")
