# Generated by Django 5.1 on 2024-08-17 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_agency_number_doc_alter_agency_opened_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='number_doc',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='agency',
            name='opened_doc',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
