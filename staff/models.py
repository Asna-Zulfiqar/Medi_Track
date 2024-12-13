from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from wards.models import Ward

class Receptionist(models.Model):
    SHIFT_CHOICES = [
        ('12:00 AM - 8:00 AM', '12:00 AM - 8:00 AM'),
        ('8:00 AM - 4:00 PM', '8:00 AM - 4:00 PM'),
        ('4:00 PM - 12:00 AM', '4:00 PM - 12:00 AM'),
        ('SPARE', 'Spare'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receptionist_profile')
    age = models.IntegerField(default=0)
    contact_number = models.CharField(max_length=15, unique=True)
    shift = models.CharField(max_length=20, choices= SHIFT_CHOICES, blank=True)
    is_available = models.BooleanField(default=True)

    def clean(self):
        if not self.user.groups.filter(name="Receptionist").exists():
            raise ValidationError("This user is not in the Receptionist group.")
        super().clean()

    def save(self, *args, **kwargs):
        # Get the count of all existing receptionists
        all_receptionists = Receptionist.objects.all()
        if self.pk is None and all_receptionists.count() >= 4:
            raise ValidationError("Cannot have more than 4 receptionists.")

        # Automatically assign the last receptionist the remaining shift
        if self.pk is None and all_receptionists.count() == 3:
            remaining_shifts = {shift[0] for shift in self.SHIFT_CHOICES} - {r.shift for r in all_receptionists}
            if len(remaining_shifts) == 1:
                self.shift = remaining_shifts.pop()

        # Validate that the shift is not already taken (except SPARE)
        if self.shift != 'SPARE' and Receptionist.objects.filter(shift=self.shift).exclude(pk=self.pk).exists():
            raise ValidationError(f"Shift {self.get_shift_display()} is already assigned to another receptionist.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.get_shift_display()})"


class SecurityGuard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_guard_profile')
    age = models.IntegerField(default=0)
    contact = models.CharField(max_length=15)
    shift_timings = models.CharField(
        choices=[
            ('12:00 PM - 8:00 AM', '12:00 PM - 8:00 AM'),
            ('8:00 AM - 4:00 PM', '8:00 AM - 4:00 PM'),
            ('4:00 PM - 12:00 PM', '4:00 PM - 12:00 PM'),
        ],
        default='12:00 PM - 8:00 AM', max_length=30
    )
    is_available = models.BooleanField(default=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='security_guards' , null=True, blank=True)

    def clean(self):
        if not self.user.groups.filter(name="SecurityGuard").exists():
            raise ValidationError("This user is not in the SecurityGuard group.")
        super().clean()

    def __str__(self):
        return f"Security Guard {self.user.username} - Shift: {self.shift_timings}"


class Sweeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sweeper_profile')
    age = models.IntegerField(default=0)
    contact = models.CharField(max_length=15)
    shift_timings = models.CharField(
        choices=[
            ('12:00 PM - 8:00 AM', '12:00 PM - 8:00 AM'),
            ('8:00 AM - 4:00 PM', '8:00 AM - 4:00 PM'),
            ('4:00 PM - 12:00 PM', '4:00 PM - 12:00 PM'),
        ],
        default='12:00 PM - 8:00 AM', max_length=30
    )
    is_available = models.BooleanField(default=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='sweepers' , null=True , blank=True)

    def clean(self):
        if not self.user.groups.filter(name="Sweeper").exists():
            raise ValidationError("This user is not in the Sweeper group.")
        super().clean()

    def __str__(self):
        return f"Sweeper {self.user.username} - Shift: {self.shift_timings}"

class Nurse(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='nurse_profile'
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
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE , related_name='nurses' , null=True , blank=True)
    contact = models.CharField(max_length=15)
    experience = models.IntegerField()
    # Shift times
    time_slots = [
        ('12:00 PM - 8:00 AM', '12:00 PM - 8:00 AM'),
        ('8:00 AM - 4:00 PM' , '8:00 AM - 4:00 PM'),
        ('4:00 PM - 12:00 PM', '4:00 PM - 12:00 PM'),
    ]
    shift_timings = models.CharField(choices=time_slots, default='12:00 PM - 8:00 AM', max_length=30)

    # Availability status
    is_available = models.BooleanField(default=True)

    def clean(self):
        # Ensure that the user is in the "Doctors" group
        if not self.user.groups.filter(name="Nurse").exists():
            raise ValidationError("This user is not in the Nurse group.")
        super().clean()

    def __str__(self):
        return f"Doctor {self.user.username} - {self.specialization}"
