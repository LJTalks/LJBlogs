from django.db import models
from cloudinary.models import CloudinaryField


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    project_image_cloudinary = CloudinaryField(
        'image', null=True, blank=True, default='default-placeholder.png')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
