
from rest_framework import serializers
from .models import Project
from portfolio.serializers import MediaValidationMixin


class ProjectSerializer(MediaValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def validate(self, attrs):
        live = attrs.get(
            "live_url", getattr(self.instance, "live_url", "")
        )
        github = attrs.get(
            "github_url", getattr(self.instance, "github_url", "")
        )

        if not live and not github:
            raise serializers.ValidationError(
                "Provide at least one live URL or GitHub URL."
            )
        return attrs
