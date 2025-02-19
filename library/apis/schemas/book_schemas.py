from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from books.serializers import BookSerializer


book_detail_schema = extend_schema_view(
    get=extend_schema(
        summary="Retrieve a Book by ID or Slug",
        description="Fetch a single book using either its ID or its slug.",
        parameters=[
            OpenApiParameter(
                name="identifier",
                description="Book ID (integer) or Slug (string)",
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={200: BookSerializer},
    )
)