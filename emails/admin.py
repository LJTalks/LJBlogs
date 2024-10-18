from django.contrib import admin
from .models import EmailListSubscriber, ListType


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


# Register ListType model in the admin panel
@admin.register(ListType)
class ListTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Show the name and description of each list type
    search_fields = ('name',)  # Allow admins to search by name