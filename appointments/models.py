from django.utils import timezone
from django.db import models
from rest_framework.exceptions import ValidationError
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment for {self.patient.user.username} with Dr. {self.doctor.user.username} on {self.appointment_date}"

    def mark_as_completed(self):
        """Mark the appointment as completed."""
        self.status = 'completed'
        self.save()

    def mark_as_cancelled(self):
        """Mark the appointment as cancelled."""
        self.status = 'cancelled'
        self.save()

    def mark_as_rescheduled(self, new_appointment_date):
        """Mark the appointment as rescheduled."""
        self.status = 'rescheduled'
        self.appointment_date = new_appointment_date
        self.save()

    def save(self, *args, **kwargs):
        """Custom save method to ensure the appointment date is not in the past."""
        if self.appointment_date < timezone.now():
            raise ValidationError("Appointment date cannot be in the past.")

        super().save(*args, **kwargs)




