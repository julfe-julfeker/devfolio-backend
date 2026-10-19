
import math
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("PUBLISHED", "Published"),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="blog/")

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    published_at = models.DateTimeField(null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            max_length = self._meta.get_field("slug").max_length

            base_slug = base_slug[:max_length].rstrip("-")
            candidate = base_slug
            counter = 2

            while Post.objects.filter(slug=candidate).exclude(
                pk=self.pk
            ).exists():
                suffix = f"-{counter}"
                candidate = (
                    base_slug[:max_length - len(suffix)].rstrip("-")
                    + suffix
                )
                counter += 1

            self.slug = candidate

        words = len(self.content.split())
        self.reading_time = max(1, math.ceil(words / 200))

        if self.status == "PUBLISHED" and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
