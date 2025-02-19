from django.urls import path

from .views import BooksAPIView, BookDetailAPIView


urlpatterns = [
    path(
        "books/", 
        BooksAPIView.as_view(), 
        name="books"
    ),
    path(
        "books/<str:id_or_slug>/", 
        BookDetailAPIView.as_view(), 
        name="book_detail"
    ),
]
