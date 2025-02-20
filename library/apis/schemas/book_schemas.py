from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from books.serializers import BookSerializer


book_detail_schema = extend_schema_view(
    get=extend_schema(
        summary="Retrieve a Book by ID or Slug",
        description="Fetch a single book using either its ID (integer) or slug (string).",
        parameters=[
            OpenApiParameter(
                name="id_or_slug",
                description="Book ID (integer) or Slug (string)",
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={200: BookSerializer, 404: {"description": "Book not found"}},
    ),
    patch=extend_schema(
        summary="Update a Book (Partial)",
        description="Update a book using either its ID or slug. Allows partial updates.",
        parameters=[
            OpenApiParameter(
                name="id_or_slug",
                description="Book ID (integer) or Slug (string)",
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        request=BookSerializer,
        responses={200: BookSerializer, 400: {"description": "Invalid data"}},
    ),
    delete=extend_schema(
        summary="Delete a Book",
        description="Delete a book using either its ID or slug.",
        parameters=[
            OpenApiParameter(
                name="id_or_slug",
                description="Book ID (integer) or Slug (string)",
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={204: {"description": "Book deleted successfully"}, 404: {"description": "Book not found"}},
    ),
)
