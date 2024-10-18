from django.db import models
from django.contrib.auth.models import User


class ListType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class EmailListSubscriber(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)  # Tied to User for registered users
    list_email = models.EmailField(null=True, blank=True)  # For unregistered
    list_type = models.ManyToManyField(ListType)
    source = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{
            self.list_email or self.user.email} - {
                ', '.join([lt.name for lt in self.list_type.all()])}"
