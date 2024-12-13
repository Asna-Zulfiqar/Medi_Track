from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from medical_records.models import LabPrescription
from patients.models import Patient


class Laboratory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lab_tech_profile")
    lab_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()

    def clean(self):
        # Ensure the user is in the "Lab Technician" group
        if not self.user.groups.filter(name="Lab Technician").exists():
            raise ValidationError("Only users in the 'Lab Technician' group can create a Laboratory.")

        if self.opening_hours >= self.closing_hours:
            raise ValidationError("Opening hours must be before closing hours.")

    def is_open(self):
        current_time = now().time()
        return self.opening_hours <= current_time <= self.closing_hours

    def __str__(self):
        return self.lab_name


class Test(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name="tests")
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField()

    def clean(self):

        if self.duration <= 0:
            raise ValidationError("Duration must be a positive number.")

    def __str__(self):
        return self.test_name


class LabTestAllocation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="lab_tests")
    prescription = models.ForeignKey(LabPrescription, on_delete=models.CASCADE, related_name='allocations')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='lab_test_allocations')
    allocated_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('allocated', 'Allocated'), ('completed', 'Completed')], default='allocated')

    def __str__(self):
        return f"Lab Test Allocation for {self.prescription.test.test_name} - {self.laboratory.lab_name}"