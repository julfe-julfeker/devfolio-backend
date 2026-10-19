
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    full_name = models.CharField(max_length=150)
    headline = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)

    years_of_experience = models.PositiveIntegerField(default=0)
    is_available_for_hire = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValueError("Only one profile is allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("FRONTEND", "Frontend"),
        ("BACKEND", "Backend"),
        ("DATABASE", "Database"),
        ("DEVOPS", "DevOps"),
        ("TOOLS", "Tools"),
        ("SOFT_SKILL", "Soft Skill"),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    icon = models.CharField(max_length=100, blank=True)
    display_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Experience(models.Model):
    EMPLOYMENT_CHOICES = [
        ("FULL_TIME", "Full Time"),
        ("PART_TIME", "Part Time"),
        ("INTERNSHIP", "Internship"),
        ("FREELANCE", "Freelance"),
        ("CONTRACT", "Contract"),
    ]

    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_CHOICES
    )
    location = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    company_url = models.URLField(blank=True)
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.role} - {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"

