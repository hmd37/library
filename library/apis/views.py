import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.schemas.book_schemas import book_detail_schema
from books.models import Book
from books.serializers import BookSerializer

logger = logging.getLogger("django.request")


class BooksAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    ordering_fields = ["title", "published_date"]
    ordering = ["published_date"]
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        logger.info(f"[{request.method}] {request.path} - Book list requested by {request.user}")
        response = super().get(request, *args, **kwargs)
        logger.info(f"[{request.method}] {request.path} - Returned {len(response.data['results'])} books")
        return response


@book_detail_schema
class BookDetailAPIView(APIView):
    def get_book(self, id_or_slug):
        """Helper function to get a book by ID or Slug."""
        if id_or_slug.isdigit():
            return get_object_or_404(Book, id=int(id_or_slug))
        return get_object_or_404(Book, slug=id_or_slug)
    
    def get(self, request, id_or_slug):
        logger.info(f"[{request.method}] {request.path} - Book detail requested: id_or_slug={id_or_slug}")

        try:
            book = self.get_book(id_or_slug)
            serializer = BookSerializer(book)
            logger.info(f"[{request.method}] {request.path} - Book found: {book.title} (ID: {book.id}, Slug: {book.slug})")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"[{request.method}] {request.path} - Error retrieving book with id_or_slug {id_or_slug}: {str(e)}")
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id_or_slug):
        book = self.get_book(id_or_slug)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id_or_slug):
        book = self.get_book(id_or_slug)
        book.delete()
        return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
