from django.contrib import admin
from .models import Booking

# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date')
    list_filter = ('service', 'date')  # Filter in side bar
    search_fields = ('user_username', 'service_name')


admin.site.register(Booking)
