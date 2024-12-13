# Generated by Django 5.1.3 on 2024-12-02 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_receptionist'),
    ]

    operations = [
        migrations.AddField(
            model_name='receptionist',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='receptionist',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
