from django.db import models
from django.contrib.auth.models import User

# Create the post (Post Detail) models here.

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_detail"
    )
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    # SEO Tags for the blog post (Commented out until the tags model is made)
    seo_tags = models.TextField(
        blank=True, help_text="Add your SEO keywords, separated by commas")
    # Foreign key to link blog posts directly to services offered
    # (Commented out until service model is added)
    # service = models.ForeignKey(
    #     'services.Service', on_delete=models.SET_NULL, null=True, blank=True,
    #     related_name="posts")

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    # If the commenter deletes their profile, their comments will remain but
    # author field will be null
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments_author"
    )

    body = models.TextField(max_length=500)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    # Display first 50 characters in the admin panel. Check if this string
    # supplies the comment in other views
    def __str__(self):
        return f"{self.author} | {self.body[:50]}..."
