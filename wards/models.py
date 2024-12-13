from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class Ward(models.Model):
    WARD_TYPES = [
        ('ICU', 'Intensive Care Unit'),
        ('General', 'General Ward'),
        ('Maternity', 'Maternity Ward'),
        ('Pediatric', 'Pediatric Ward'),
        ('Orthopedic', 'Orthopedic Ward'),
        ('Cardiology', 'Cardiology Ward'),
        ('Neurology', 'Neurology Ward'),
        ('Surgical', 'Surgical Ward'),
        ('Psychiatric', 'Psychiatric Ward'),
        ('Emergency', 'Emergency Ward'),
        ('Burns', 'Burns Ward'),
        ('Isolation', 'Isolation Ward'),
        ('Rehabilitation', 'Rehabilitation Ward'),
        ('Geriatrics', 'Geriatrics Ward'),
        ('Oncology', 'Oncology Ward'),
        ('Urology', 'Urology Ward'),
        ('Nephrology', 'Nephrology Ward'),
        ('Plastic', 'Plastic Surgery Ward'),
        ('ENT', 'Ear, Nose, and Throat Ward'),
        ('Respiratory', 'Respiratory Ward'),
        ('Trauma', 'Trauma Ward'),
        ('Dialysis', 'Dialysis Ward'),
        ('Intensive', 'Intensive Care Ward'),
    ]

    ward_type = models.CharField(max_length=100, choices=WARD_TYPES, unique=True)
    capacity = models.PositiveIntegerField(default=40)
    daily_bed_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def __str__(self):
        return f"{self.get_ward_type_display()} Ward"

    def clean(self):

        # Check if another Ward with the same type already exists
        if Ward.objects.filter(ward_type=self.ward_type).exists():
            raise ValidationError(f"A ward of type '{self.get_ward_type_display()}' already exists.")

        # Making sure that the bed Count in a Ward does not exceed the capacity
        if self.pk and self.beds.count() > self.capacity:
            raise ValidationError(f"The number of beds exceeds the capacity of {self.capacity}.")

    def create_beds(self):
        #Create beds for the ward when Ward is created
        for _ in range(self.capacity):
            Bed.objects.create(ward=self, status='free')


class Bed(models.Model):
    BED_STATUS = [
        ('occupied', 'Occupied'),
        ('free', 'Free'),
        ('cleaning', 'Cleaning'),
        ('maintenance', 'Maintenance'),
    ]

    id = models.AutoField(primary_key=True)
    ward = models.ForeignKey(Ward, related_name='beds', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=BED_STATUS, default='free')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bed {self.id} ({self.get_status_display()}) in {self.ward.get_ward_type_display()} Ward"


class WardManager(models.Model):
    SHIFT_CHOICES = [
        ('00:00-08:00', '12:00 AM - 8:00 AM'),
        ('08:00-16:00', '8:00 AM - 4:00 PM'),
        ('16:00-00:00', '4:00 PM - 12:00 AM'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ward_manager_profile')
    ward = models.ForeignKey(Ward, related_name='managers', on_delete=models.CASCADE)
    shift = models.CharField(max_length=11, choices=SHIFT_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.ward.get_ward_type_display()} ({self.get_shift_display()})"

    def clean(self):

        # Ensure that a user can only be the manager of one ward at a time
        if WardManager.objects.filter(user=self.user).exclude(pk=self.pk).exists():
            raise ValidationError(f"{self.user.username} is already assigned as a manager to another ward.")

        # Ensure no more than 3 managers per ward
        if self.ward.managers.count() >= 3:
            raise ValidationError(f"The ward '{self.ward.get_ward_type_display()}' already has 3 managers.")

        # Ensure no duplicate shift assignments for the same ward
        if self.ward.managers.filter(shift=self.shift).exists():
            raise ValidationError(f"The shift '{self.get_shift_display()}' is already taken for this ward.")

    def is_within_shift(self):

        # Check if the manager is currently within their shift
        start_time, end_time = [int(t.split(":")[0]) for t in self.shift.split("-")]
        current_hour = now().hour

        if start_time < end_time:
            return start_time <= current_hour < end_time
        else:  # Handles shifts spanning midnight
            return current_hour >= start_time or current_hour < end_time

