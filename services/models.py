from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=97.00, blank=True)
# should the default price be a string? it shouldn't... does it specify the pound sign?

    def __str__(self):
        return self.name
