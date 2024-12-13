from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from patients.models import Patient


class Pharmacy(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='pharmacy'
    )
    pharmacy_name = models.CharField(max_length=255)
    email = models.EmailField()
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    contact = models.CharField(max_length=15)

    def clean(self):
        # Ensure the user is in the "Pharmacist" group
        if not self.user.groups.filter(name="Pharmacist").exists():
            raise ValidationError("Only users in the 'Pharmacist' group can create a pharmacy.")

    def is_open(self):
        current_time = now().time()
        return self.opening_hours <= current_time <= self.closing_hours

    def __str__(self):
        return self.pharmacy_name

class Medicine(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='medicines')
    medicine_name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0 , validators=[MinValueValidator(0)])
    expiration_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reorder_level = models.IntegerField(default=10 , validators=[MinValueValidator(0)])

    def is_expired(self):
        return self.expiration_date < now().date()

    def needs_reorder(self):
        return self.stock <= self.reorder_level

    def __str__(self):
        return f"{self.medicine_name} - {self.pharmacy.pharmacy_name}"


class MedicineAllocation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="allocations")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="allocations")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="allocations")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.username} - {self.medicine.medicine_name} - {self.quantity}"
