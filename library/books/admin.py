from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_date"]
    prepopulated_fields = {"slug": ("title", "author")}


admin.site.register(Book, BookAdmin)
