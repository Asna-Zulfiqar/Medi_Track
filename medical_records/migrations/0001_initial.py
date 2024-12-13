# Generated by Django 5.1.3 on 2024-11-28 10:50

import django.db.models.deletion
import medical_records.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0003_remove_doctor_shift_end_time_and_more'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabPrescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=255)),
                ('prescribed_on', models.DateField(auto_now_add=True)),
                ('instructions', models.TextField(blank=True, null=True)),
                ('prescribed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_prescriptions', to='doctors.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='MedicinePrescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=255)),
                ('dosage', models.CharField(max_length=100)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('prescribed_on', models.DateField(auto_now_add=True)),
                ('prescribed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicine_prescriptions', to='doctors.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('test_date', models.DateField(auto_now_add=True)),
                ('file', models.FileField(upload_to='test_results/', validators=[medical_records.models.validate_pdf])),
                ('lab_prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_records.labprescription')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField(auto_now_add=True)),
                ('doctor_notes', models.TextField(blank=True, null=True)),
                ('lab_prescriptions', models.ManyToManyField(blank=True, related_name='medical_records', to='medical_records.labprescription')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
                ('medicines_prescribed', models.ManyToManyField(blank=True, related_name='medical_records', to='medical_records.medicineprescription')),
                ('test_results', models.ManyToManyField(blank=True, related_name='medical_records', to='medical_records.testresult')),
            ],
        ),
    ]