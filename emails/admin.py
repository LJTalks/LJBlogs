from django.contrib import admin
from .models import EmailListSubscriber


@admin.register(EmailListSubscriber)
class EmailListSubscriberAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'list_type', 'date_joined', 'source')
    list_filter = ('list_type', 'date_joined')  # Optional filtering options
    search_fields = ('user__email',)

    # Add a method to access the email from the related user
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    # Optional: Add filters if `list_type` or `date_joined` is relevant
    list_filter = ('list_type', 'date_joined')

