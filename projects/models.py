
from django.db import models
from django.utils.text import slugify
from portfolio.models import Skill


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("WEB", "Web"),
        ("MOBILE", "Mobile"),
        ("API", "API"),
        ("ML", "Machine Learning"),
        ("OTHER", "Other"),
    ]

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    summary = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="projects/")
    tech_stack = models.ManyToManyField(Skill, related_name="projects")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    completed_date = models.DateField()
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-completed_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
