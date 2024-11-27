from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()

    def clean(self):
        # Ensure that the user is in the "Patient" group
        if not self.user.groups.filter(name="Patient").exists():
            raise ValidationError("This user is not in the Patient group.")
        super().clean()

    def __str__(self):
        return f"Patient {self.user.username}"

class Condition(models.Model):
    condition = models.CharField(max_length=100)
    diagnosis_date = models.DateField()
    treatment_details = models.TextField()

    def __str__(self):
        return self.condition

class Allergy(models.Model):
    allergy = models.CharField(max_length=100)

    def __str__(self):
        return self.allergy

class Surgery(models.Model):
    surgery = models.CharField(max_length=100)
    surgery_date = models.DateField()

    def __str__(self):
        return self.surgery


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    conditions = models.ManyToManyField(Condition, blank=True)
    allergies = models.ManyToManyField(Allergy, blank=True)
    surgeries = models.ManyToManyField(Surgery, blank=True)

    def __str__(self):
        return f"Medical History of {self.patient.user.username}"
