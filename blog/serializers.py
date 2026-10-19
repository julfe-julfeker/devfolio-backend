
from rest_framework import serializers

from .models import Category, Tag, Post
from portfolio.serializers import MediaValidationMixin


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = (
            "id",
            "slug",
            "created_at",
            "updated_at",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = (
            "id",
            "slug",
            "created_at",
            "updated_at",
        )


class PostSerializer(
    MediaValidationMixin,
    serializers.ModelSerializer
):
    likes_count = serializers.IntegerField(
        read_only=True,
        default=0
    )

    comments_count = serializers.IntegerField(
        read_only=True,
        default=0
    )

    class Meta:
        model = Post
        fields = "__all__"

        read_only_fields = (
            "id",
            "slug",
            "author",
            "published_at",
            "views_count",
            "reading_time",
            "created_at",
            "updated_at",
        )

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Title must contain at least 5 characters."
            )

        return value

    def validate(self, attrs):
        post_status = attrs.get(
            "status",
            getattr(self.instance, "status", "DRAFT")
        )

        content = attrs.get(
            "content",
            getattr(self.instance, "content", "")
        )

        category = attrs.get(
            "category",
            getattr(self.instance, "category", None)
        )

        if post_status == "PUBLISHED":
            if len(content.strip()) < 100:
                raise serializers.ValidationError({
                    "content": (
                        "Published posts need at least "
                        "100 characters."
                    )
                })

            if not category:
                raise serializers.ValidationError({
                    "category": (
                        "Category is required to publish."
                    )
                })

        return attrs
