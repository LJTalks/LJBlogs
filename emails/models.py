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
                

class SiteContactInfo(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Site Contact Info"
        verbose_name_plural = "Site Contact Info"
       
       
class NewsletterEmail(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_send_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.subject
    