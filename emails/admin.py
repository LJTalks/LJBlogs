from django.contrib import admin
from .models import (
    EmailListSubscriber,
    ListType,
    SiteContactInfo,
    NewsletterEmail
)
from django_summernote.admin import SummernoteModelAdmin
from django.db import models


@admin.register(EmailListSubscriber)
class EmailListSubscriberAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'get_list_types', 'date_joined', 'source')
    list_filter = ('list_type', 'date_joined')  # Optional filtering options
    search_fields = ('user__email', 'list_email')
    
    # Show user email if the user exists
    def user_email(self, obj):
        return obj.user.email if obj.user else obj.list_email
    user_email.short_description = 'User Email'
    
    def get_list_types(self, obj):
        return ", ".join([lt.name for lt in obj.list_type.all()])
    get_list_types.short_description = "Subscribed List Types"


class SentEmailLog(models.Model):
    newsletter = models.ForeignKey(NewsletterEmail, on_delete=models.CASCADE)
    recipient = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)


class NewsletterEmailAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)


admin.site.register(NewsletterEmail, NewsletterEmailAdmin)
# Register the SiteContactInfo model in the email admin panel
admin.site.register(SiteContactInfo)


# Register ListType model in the admin panel
@admin.register(ListType)
class ListTypeAdmin(admin.ModelAdmin):
    # Show name and description of each list type
    list_display = ('name', 'description')
    search_fields = ('name',)  # Allow admins to search by name