# Generated by Django 5.1 on 2024-08-13 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_trackingevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('agency_name', models.CharField(max_length=256)),
                ('Mobilenumber', models.CharField(max_length=50)),
                ('number_doc', models.PositiveIntegerField(blank=True, null=True)),
                ('opened_doc', models.PositiveIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
