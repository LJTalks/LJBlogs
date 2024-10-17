from django.db import models


class EmailListSubscriber(models.Model):
        EMAIL_PREFERENCE_CHOICES = [
        ('weekly', 'Weekly Updates'),
        ('news', 'News and Important Changes'),
    ]
        
        email = models.EmailField(unique=True)
        source = models.CharField(max_length=255, null=True, blank=True)
        date_joined = models.DateTimeField(auto_now_add=True)
        preferences = models.CharField(
            max_length=10,
            choices=EMAIL_PREFERENCE_CHOICES,
            default='weekly'  # Default preference for new subscribers
        )

        def __str__(self):
            return self.email
