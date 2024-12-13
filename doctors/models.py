from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from wards.models import Ward

class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='doctor_profile'
    )
    age = models.IntegerField(default=0)
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative'),
        ('ABO' , 'Blood type unknown or not specified')
    ]
    blood = models.CharField(max_length=10 , blank=True , choices=BLOOD_TYPE_CHOICES , default='ABO')
    specialization = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='doctors', null=True, blank=True)
    contact = models.CharField(max_length=15)
    experience = models.IntegerField()
    # Shift times
    time_slots = [
        ('12:00 PM - 8:00 AM', '12:00 PM - 8:00 AM'),
        ('8:00 AM - 4:00 PM' , '8:00 AM - 4:00 PM'),
        ('4:00 PM - 12:00 PM', '4:00 PM - 12:00 PM'),
    ]
    shift_timings = models.CharField(choices=time_slots, default='12:00 PM - 8:00 AM', max_length=30)
    is_available = models.BooleanField(default=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=200.00)

    def clean(self):
        # Ensure that the user is in the "Doctors" group
        if not self.user.groups.filter(name="Doctor").exists():
            raise ValidationError("This user is not in the Doctor group.")
        super().clean()

    def __str__(self):
        return f"Doctor {self.user.username} - {self.specialization}"
