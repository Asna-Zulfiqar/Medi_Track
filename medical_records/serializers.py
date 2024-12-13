from rest_framework import serializers
from medical_records.models import MedicalRecord, MedicinePrescription, LabPrescription

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            'id',
            'patient',
            'emergency',
            'record_date',
            'blood_group',
            'ward_admitted_to',
            'ward_admit_date',
            'discharge_date',
            'doctor_notes',
            'diagnoses',
            'treatment_plan',
            'medicines_prescribed',
            'lab_prescriptions',
            'test_results',
            'surgeries',
        ]
        read_only_fields = ['patient', 'record_date', 'ward_admit_date']

class MedicinePrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinePrescription
        fields = '__all__'
        read_only_fields = ['prescribed_by', 'prescribed_on']

class LabPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabPrescription
        fields = ['id', 'test', 'prescribed_by', 'prescribed_on', 'test_instructions', 'patient']
        read_only_fields = ['prescribed_by', 'prescribed_on']

