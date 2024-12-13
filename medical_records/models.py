from django.db import models
from rest_framework.exceptions import ValidationError
from patients.models import Patient
from doctors.models import Doctor
from wards.models import Ward

class LabPrescription(models.Model):
    test = models.ForeignKey('laboratory.Test', on_delete=models.CASCADE, related_name='prescriptions' , null=True , blank=True)  # Link to Test
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='lab_prescriptions')
    prescribed_on = models.DateField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_prescriptions' , null=True, blank=True)
    test_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lab Prescription for {self.test} - {self.patient.user.username}"


class MedicinePrescription(models.Model):
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(blank=True, null=True)
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medicine_prescriptions')
    prescribed_on = models.DateField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medicine_prescriptions' , null=True , blank=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.medicine_name} ({self.dosage}) - {self.patient.user.username}"


def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

class Surgery(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='surgeries')
    surgery_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    surgery_date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , blank=True, null=True , related_name='surgeon_name')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.surgery_name} - {self.doctor} ({self.surgery_date})"

class TestResult(models.Model):
    lab_prescription = models.ForeignKey(LabPrescription, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    result = models.TextField()
    test_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to="test_results/" , validators=[validate_pdf])

    def __str__(self):
        return f"Test Result for {self.patient} - {self.lab_prescription.test.test_name} on {self.test_date}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='medical_record')
    emergency = models.BooleanField(default=False)
    record_date = models.DateField(auto_now_add=True)
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative'),
        ('ABO', 'Blood type unknown or not specified'),
    ]
    blood_group = models.CharField(max_length=10 , null=True, blank=True , choices=BLOOD_TYPE_CHOICES)
    ward_admitted_to = models.ForeignKey(Ward, on_delete=models.CASCADE , related_name='admitted_ward' , null=True, blank=True)
    ward_admit_date = models.DateField(auto_now_add=True , null=True, blank=True)
    discharge_date = models.DateField(null=True , blank=True)
    doctor_notes = models.TextField(blank=True, null=True)
    diagnoses = models.TextField(blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    medicines_prescribed = models.ManyToManyField('MedicinePrescription', related_name='medical_records', blank=True)
    lab_prescriptions = models.ManyToManyField('LabPrescription', related_name='medical_records', blank=True)
    test_results = models.ManyToManyField('TestResult', related_name='medical_records', blank=True)
    surgeries = models.ForeignKey(Surgery, on_delete=models.CASCADE, related_name='surgeries_performed', blank=True , null=True)

    def __str__(self):
        return f"Medical Record for {self.patient} on {self.record_date}"
