# Generated by Django 5.1.3 on 2024-12-10 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_records', '0005_labprescription_test_instructions_and_more'),
        ('patients', '0004_alter_patient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_record', to='patients.patient'),
        ),
    ]
