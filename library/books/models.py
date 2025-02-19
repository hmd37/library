from django.db import models
from django.utils.text import slugify


class Book(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(default="", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title} {self.author}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
