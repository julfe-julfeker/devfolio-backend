
from rest_framework import serializers
from django.utils import timezone
from PIL import Image, UnidentifiedImageError

from .models import Profile, Skill, Experience, Education


class MediaValidationMixin:
    IMAGE_MAX_SIZE = 2 * 1024 * 1024
    RESUME_MAX_SIZE = 5 * 1024 * 1024

    ALLOWED_IMAGE_EXTENSIONS = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    ALLOWED_IMAGE_FORMATS = (
        "JPEG",
        "PNG",
        "WEBP",
    )

    def validate_avatar(self, file):
        return self.validate_image(file)

    def validate_cover_image(self, file):
        return self.validate_image(file)

    def validate_image(self, file):
        if not file:
            return file

        if file.size > self.IMAGE_MAX_SIZE:
            raise serializers.ValidationError(
                "Image must not exceed 2 MB."
            )

        if not file.name.lower().endswith(
            self.ALLOWED_IMAGE_EXTENSIONS
        ):
            raise serializers.ValidationError(
                "Only JPG, PNG and WebP images are allowed."
            )

        try:
            file.seek(0)

            image = Image.open(file)
            image_format = image.format
            image.verify()

            if image_format not in self.ALLOWED_IMAGE_FORMATS:
                raise serializers.ValidationError(
                    "Unsupported image format."
                )

        except serializers.ValidationError:
            raise

        except (
            UnidentifiedImageError,
            OSError,
            ValueError,
        ):
            raise serializers.ValidationError(
                "Invalid or corrupted image."
            )

        finally:
            file.seek(0)

        return file

    def validate_resume(self, file):
        if not file:
            return file

        if file.size > self.RESUME_MAX_SIZE:
            raise serializers.ValidationError(
                "Resume must not exceed 5 MB."
            )

        if not file.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Resume must be a PDF."
            )

        try:
            file.seek(0)

            if file.read(5) != b"%PDF-":
                raise serializers.ValidationError(
                    "Invalid PDF file."
                )

        finally:
            file.seek(0)

        return file


class ProfileSerializer(
    MediaValidationMixin,
    serializers.ModelSerializer
):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

    def validate_proficiency(self, value):
        if not 1 <= value <= 100:
            raise serializers.ValidationError(
                "Proficiency must be between 1 and 100."
            )

        return value


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

    def validate(self, attrs):
        start = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        end = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None)
        )

        current = attrs.get(
            "is_current",
            getattr(self.instance, "is_current", False)
        )

        if start and start > timezone.localdate():
            raise serializers.ValidationError({
                "start_date": "Start date cannot be in the future."
            })

        if current and end:
            raise serializers.ValidationError({
                "end_date": (
                    "Current employment must not have an end date."
                )
            })

        if not current and not end:
            raise serializers.ValidationError({
                "end_date": "End date is required."
            })

        if start and end and end <= start:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })

        return attrs


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
