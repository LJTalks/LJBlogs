from django.db import models
from django.contrib.auth.models import User


# Move this to user_profile app when it exists
# We want to see where the bots are getting in 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255, blank=True, null=True)
    # Optional: track IP
    registration_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
