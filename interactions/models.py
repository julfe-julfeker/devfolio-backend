
from django.db import models
from blog.models import Post


class PostLike(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    visitor_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "visitor_id")

    def __str__(self):
        return f"{self.post.title} - {self.visitor_id}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.post.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
