# Generated by Django 5.1 on 2024-08-17 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_agency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='Mobilenumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
