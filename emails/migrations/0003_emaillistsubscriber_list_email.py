# Generated by Django 4.2.13 on 2024-10-18 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_remove_emaillistsubscriber_list_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillistsubscriber',
            name='list_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]