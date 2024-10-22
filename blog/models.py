from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.html import strip_tags


# Blog post (Post Detail) models here.
STATUS = ((0, "Draft"), (1, "Published"))


class ViewRecord(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='view_records')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} viewed {self.post.title} on {self.viewed_on}"


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_detail"
    )
    featured_image = CloudinaryField(
        'image', null=True, blank=True, default='placeholder'
        )
    alt_text = models.CharField(
        max_length=255, blank=True, help_text="Alt text for image")
    image_credit = models.CharField(
        max_length=255, blank=True, help_text="Credit for the image")
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    publish_date = models.DateTimeField(blank=True, null=True)
    viewed_by = models.ManyToManyField(
        User, related_name='viewed_posts', blank=True)
    views = models.IntegerField(default=0)  # New field for tracking post views
    # SEO Tags for the blog post
    seo_tags = models.TextField(
        blank=True, help_text="Add your SEO keywords, separated by commas")
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Add short, relevant SEO meta description"
    )
    
    @property
    def meta_description_with_fallback(self):
        # Return meta description if available, or fallback to post content
        if self.meta_description:
            return self.meta_description
        else:
            # Fallback: strip html tags and truncate post content 160 chars
            return strip_tags(self.content)[:160]
    # Foreign key to link blog posts directly to services offered
    # (Commented out until service model is added)
    # service = models.ForeignKey(
    #     'services.Service', on_delete=models.SET_NULL, null=True, blank=True,
    #     related_name="posts")
    

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | {self.author}"


# BlogComments (in blog Post Detail) models here.
BLOG_COMMENT_STATUS = ((0, "Submitted"), (1, "Approved"))


class BlogComment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="blog_comments"
    )
    # If the commenter deletes their profile, their comments will remain but
    # author field will be null - maybe need to give a "deleted user" name?
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name="blog_comments_author"
    )
    body = models.TextField(max_length=500)
    status = models.IntegerField(choices=BLOG_COMMENT_STATUS, default=0) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    # Display first 50 characters in the admin panel. Check if this string
    # supplies the comment in other views
    def __str__(self):
        return f"{self.author} | {self.body[:50]}..."
