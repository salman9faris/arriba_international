# Generated by Django 5.1 on 2024-08-31 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_userprofile_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='tracking',
            field=models.BooleanField(default=True),
        ),
    ]
