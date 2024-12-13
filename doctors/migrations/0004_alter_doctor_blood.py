# Generated by Django 5.1.3 on 2024-11-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_remove_doctor_shift_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='blood',
            field=models.CharField(blank=True, choices=[('A+', 'A Positive'), ('A-', 'A Negative'), ('B+', 'B Positive'), ('B-', 'B Negative'), ('AB+', 'AB Positive'), ('AB-', 'AB Negative'), ('O+', 'O Positive'), ('O-', 'O Negative'), ('ABO', 'Blood type unknown or not specified')], default='ABO', max_length=10),
        ),
    ]
