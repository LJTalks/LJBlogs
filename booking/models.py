from django.db import models
from services.models import Service
from django.contrib.auth.models import User

# Create the Bookings models here.


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    date = models.DateField()  # Date of booking
    time = models.TimeField()  # Time of booking
    # Optional: additional details from the client
    message = models.TextField(null=False)
    # For marking bookings as confirmed
    confirmed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.service.title} on {self.date}"
