from django.db import models
from django.contrib.auth.models import User

class Leave(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.status == 'Approved':
            profile = None
            if hasattr(self.user, 'nurse_profile'):
                profile = self.user.nurse_profile
            elif hasattr(self.user, 'doctor_profile'):
                profile = self.user.doctor_profile
            elif hasattr(self.user, 'security_profile'):
                profile = self.user.security_profile
            elif hasattr(self.user, 'sweeper_profile'):
                profile = self.user.sweeper_profile
            elif hasattr(self.user, 'lab_tech_profile'):
                profile = self.user.lab_tech_profile
            elif hasattr(self.user, 'ward_manager_profile'):
                profile = self.user.ward_manager_profile

            if profile:
                profile.is_available = False
                profile.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Leave ({self.user.username}) - {self.status}"
