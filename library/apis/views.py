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


class BookListAPIView(ListCreateAPIView):
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
    def get(self, request, identifier):
        logger.info(f"[{request.method}] {request.path} - Book detail requested: identifier={identifier}")

        try:
            if identifier.isdigit():
                book = get_object_or_404(Book, id=int(identifier))
            else:
                book = get_object_or_404(Book, slug=identifier)

            serializer = BookSerializer(book)
            logger.info(f"[{request.method}] {request.path} - Book found: {book.title} (ID: {book.id}, Slug: {book.slug})")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"[{request.method}] {request.path} - Error retrieving book with identifier {identifier}: {str(e)}")
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
