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


class ClientIntake(models.Model):
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    competitors = models.TextField(blank=True, null=True)
    # Stores selected purposes as a comma-separated string
    purpose = models.CharField(max_length=255)

    def __str__(self):
        return self.business_name
