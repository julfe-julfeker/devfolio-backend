
from rest_framework import serializers
from .models import Comment, ContactMessage, PostLike


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id", "post", "name", "email", "website",
            "content", "parent", "is_approved",
            "created_at", "updated_at", "replies",
        ]
        read_only_fields = [
            "id", "is_approved", "created_at",
            "updated_at", "replies",
        ]

    def get_replies(self, obj):
        replies = obj.replies.filter(is_approved=True)
        return [
            {
                "id": reply.id,
                "name": reply.name,
                "content": reply.content,
                "created_at": reply.created_at,
            }
            for reply in replies
        ]

    def validate(self, attrs):
        parent = attrs.get("parent")
        post = attrs.get("post")

        if parent:
            if parent.parent_id:
                raise serializers.ValidationError(
                    "Only one level of replies is allowed."
                )

            if parent.post_id != post.id:
                raise serializers.ValidationError(
                    "Reply must belong to the same post."
                )

        return attrs


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = [
            "id", "is_read", "created_at", "updated_at"
        ]


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"
