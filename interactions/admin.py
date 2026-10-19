from django.contrib import admin
from .models import PostLike, Comment, ContactMessage

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("post", "visitor_id", "created_at")
    search_fields = ("visitor_id",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "is_approved", "created_at")
    search_fields = ("name", "content")
    list_filter = ("is_approved",)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    search_fields = ("name", "email", "subject")
    list_filter = ("is_read",)