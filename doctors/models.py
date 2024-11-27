from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError

class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='doctor_profile'
    )
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    experience = models.IntegerField()

    def clean(self):
        # Ensure that the user is in the "Doctors" group
        if not self.user.groups.filter(name="Doctor").exists():
            raise ValidationError("This user is not in the Doctor group.")
        super().clean()

    def __str__(self):
        return f"Doctor {self.user.username} - {self.specialization}"
