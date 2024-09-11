from django.db import models
from django.contrib.auth.models import User

# Create the post (Blog Post) models here.

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    # Foreign key to link blog posts directly to services offered
    # Commented out until service model is added
    # service = models.ForeignKey(
    # Service, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
