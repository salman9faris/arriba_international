# Generated by Django 5.1 on 2024-08-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_totalcount_agency'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='status',
            field=models.CharField(default='open', max_length=25),
        ),
    ]
