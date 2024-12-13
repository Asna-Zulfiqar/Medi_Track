from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework.exceptions import ValidationError
from doctors.models import Doctor
from patients.models import Patient


class Feedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='feedback')
    reviews = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.patient.user.username} on {self.created_at}"

class DoctorFeedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='doctorfeedback')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name='feedback')
    reviews = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.patient.user.username} for Dr. {self.doctor.user.username}"


class ServiceFeedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='servicefeedback')
    service = models.CharField(max_length=200)
    reviews = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.patient.user.username} for {self.service}"


class StaffFeedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='staff_feedback')
    # Generic Foreign Key fields
    staff_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    staff_object_id = models.PositiveIntegerField()
    staff = GenericForeignKey('staff_content_type', 'staff_object_id')

    reviews = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)

    def __str__(self):
        return f"Feedback for {self.staff}"

    def clean(self):
        # Ensure the staff is one of the valid staff models
        allowed_models = ['receptionist', 'securityguard', 'sweeper', 'nurse']
        if self.staff_content_type.model not in allowed_models:
            raise ValidationError(f"Staff must be one of the following: {', '.join(allowed_models)}")