from django.urls import path

from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView


urlpatterns = [
    path(
        "books/", 
        BookListCreateAPIView.as_view(), 
        name="books"
    ),
    path(
        "books/<str:id_or_slug>/", 
        BookRetrieveUpdateDestroyAPIView.as_view(), 
        name="book_detail"
    ),
]
