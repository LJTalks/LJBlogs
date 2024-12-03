# projects/admin.py
from django.contrib import admin
from .models import Project, ClientIntake

admin.site.register(Project)
admin.site.register(ClientIntake)
