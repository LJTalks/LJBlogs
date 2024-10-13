from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.dateformat import format


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'last_login',
        'previous_last_login',
        'date_joined'
    )

    def previous_last_login(self, obj):
        # Check if last_login is None, and handle it accordingly
        if obj.last_login:
            # Logic for showing the previous login
            return format(obj.last_login, 'd/m/Y H:i')
        else:
            return 'Never logged in'

    previous_last_login.short_description = 'Previous Login'


# Unregister the old UserAdmin
admin.site.unregister(User)
# register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)
