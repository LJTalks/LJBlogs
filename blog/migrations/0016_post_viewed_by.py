# Generated by Django 4.2.13 on 2024-10-18 08:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_viewrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='viewed_by',
            field=models.ManyToManyField(blank=True, related_name='viewed_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]