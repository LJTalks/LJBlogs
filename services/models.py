# from django.db import models
# from services.models import Service
# from django.contrib.auth.models import User

# # Create the Bookings models here.


# class Service(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.title


# # Define the Booking Model (I've definitely written this whole block before somewhere else, did I delete it?)
# class Booking(models.Model):
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()  # Booked date
#     time = models.TimeField()  # Booked time
#     message = models.TextField(null=False)
#     confirmed = models.BooleanField(default=False)
#     completed_date = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user} - {self.service.title} on {self.date}"
