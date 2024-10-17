from django.contrib.auth.models import User
from django.db import models


# ListType model representing the two distinct lists
class ListType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# EmailListSubscriber model linking a user to one or more lists
class EmailListSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # No need for email field, using User model
    list_type = models.ForeignKey(ListType, on_delete=models.CASCADE)
    source = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.list_type.name}"
