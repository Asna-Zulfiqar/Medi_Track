from django.contrib import admin
from medical_records.models import LabPrescription, MedicinePrescription, TestResult, MedicalRecord

@admin.register(LabPrescription)
class LabPrescriptionAdmin(admin.ModelAdmin):
    list_display = ('test', 'prescribed_by', 'prescribed_on' , 'patient')

@admin.register(MedicinePrescription)
class MedicinePrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'dosage', 'duration', 'prescribed_by', 'prescribed_on' , 'patient')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'lab_prescription', 'test_date', 'result', 'file')


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_date', 'doctor_notes')

