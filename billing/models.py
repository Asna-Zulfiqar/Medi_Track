from datetime import timezone
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import  User
from django.core.exceptions import ValidationError
from appointments.models import Appointment
from pharmacy.models import MedicineAllocation
from wards.models import Ward
from medical_records.models import MedicalRecord
from patients.models import Patient

class Accountant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='accountant_profile'
    )
    ward = models.ForeignKey(
        Ward, on_delete=models.CASCADE, related_name='accountants'
    )
    age = models.IntegerField(default=0)
    contact = models.CharField(max_length=15)

    # Shift times
    time_slots = [
        ('12:00 PM - 8:00 AM', '12:00 PM - 8:00 AM'),
        ('8:00 AM - 4:00 PM', '8:00 AM - 4:00 PM'),
        ('4:00 PM - 12:00 PM', '4:00 PM - 12:00 PM'),
    ]
    shift_timings = models.CharField(
        choices=time_slots, default='12:00 PM - 8:00 AM', max_length=30
    )

    is_available = models.BooleanField(default=True)

    def clean(self):
        # Ensure the user is in the Accountant group
        if not self.user.groups.filter(name="Accountant").exists():
            raise ValidationError("This user is not in the Accountant group.")

        # Limit to one accountant per shift per ward
        existing_accountants = Accountant.objects.filter(
            ward=self.ward, shift_timings=self.shift_timings
        )
        if self.pk:
            existing_accountants = existing_accountants.exclude(pk=self.pk)
        if existing_accountants.exists():
            raise ValidationError(
                f"The shift {self.get_shift_timings_display()} in ward "
                f"{self.ward.get_ward_type_display()} is already assigned."
            )

        # Limit to three accountants per ward
        if Accountant.objects.filter(ward=self.ward).exclude(pk=self.pk).count() >= 3:
            raise ValidationError(
                f"The ward {self.ward.get_ward_type_display()} already has 3 accountants."
            )
        super().clean()

    def __str__(self):
        return f"Accountant {self.user.username} - {self.ward} ({self.get_shift_timings_display()})"

class Billing(models.Model):
    patient = models.OneToOneField(
        'patients.Patient', on_delete=models.CASCADE, related_name='billing'
    )
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    bed_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    surgery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    medicine_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    lab_test_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    generated_at = models.DateTimeField(auto_now_add=True)

    def calculate_bed_fee(self):
        """Calculate the bed fee based on the ward's daily bed fee and stay duration."""
        medical_record = MedicalRecord.objects.filter(patient=self.patient).last()
        if medical_record and medical_record.ward_admitted_to and medical_record.ward_admit_date and medical_record.discharge_date:
            days_stayed = (medical_record.discharge_date - medical_record.ward_admit_date).days
            self.bed_fee = days_stayed * medical_record.ward_admitted_to.daily_bed_fee

    def calculate_surgery_fee(self):
        """Calculate surgery fee from the associated medical record's surgery."""
        medical_record = MedicalRecord.objects.filter(patient=self.patient).last()
        if medical_record and medical_record.surgeries:
            self.surgery_fee = medical_record.surgeries.price
        else:
            self.surgery_fee = 0

    def calculate_medicine_fee(self):
        """Calculate total medicine fee based on the associated medicine allocations."""
        # Fetch the last medical record of the patient
        medicine_allocations = MedicineAllocation.objects.filter(patient=self.patient)

        total_fee = Decimal('0.00')
        for allocation in medicine_allocations:
            price = Decimal(allocation.medicine.price)
            quantity = Decimal(allocation.quantity)
            total_fee += price * quantity

        self.medicine_fee = total_fee

    def calculate_discount(self):
        """Calculate the discount based on the patient's income and apply it to the total amount."""
        patient_income = self.patient.income

        if patient_income <= 20000:
            # 50% discount for low-income patients
            self.discount = Decimal('0.50')
        elif patient_income <= 50000:
            # 30% discount for medium-income patients
            self.discount = Decimal('0.30')
        else:
            # 5% discount for high-income patients
            self.discount = Decimal('0.05')

    def calculate_consultation_fee(self):
        """Calculate the total consultation fee for all appointments of the patient."""
        # Fetch all appointments for the patient
        appointments = Appointment.objects.filter(patient=self.patient)

        # Sum up the consultation fees from the doctors of all appointments
        total_fee = Decimal('0.00')
        for appointment in appointments:
            if appointment.doctor:
                total_fee += appointment.doctor.consultation_fee

        # Set the total fee
        self.consultation_fee = total_fee

    @property
    def amount_before_discount(self):
        """Return the total amount before the discount."""
        return (
                Decimal(self.consultation_fee) +
                Decimal(self.bed_fee) +
                Decimal(self.surgery_fee) +
                Decimal(self.medicine_fee) +
                Decimal(self.lab_test_fee)
        )


    def calculate_total_amount(self):
        """Calculate the total amount after applying all fees and the discount."""
        # Calculate the raw total
        raw_total = (
                Decimal(self.consultation_fee) +
                Decimal(self.bed_fee) +
                Decimal(self.surgery_fee) +
                Decimal(self.medicine_fee) +
                Decimal(self.lab_test_fee)
        )

        # Ensure the discount is a Decimal
        self.calculate_discount()

        # Apply the discount to the raw total
        self.total_amount = raw_total - (raw_total * Decimal(self.discount))

    def save(self, *args, **kwargs):
        """Ensure all fields are properly calculated and saved."""
        # Convert initial fields to Decimal for safety
        self.consultation_fee = Decimal(self.consultation_fee)
        self.bed_fee = Decimal(self.bed_fee)
        self.surgery_fee = Decimal(self.surgery_fee)
        self.medicine_fee = Decimal(self.medicine_fee)
        self.lab_test_fee = Decimal(self.lab_test_fee)
        self.discount = Decimal(self.discount)

        # Recalculate fees and total
        self.calculate_bed_fee()
        self.calculate_consultation_fee()
        self.calculate_surgery_fee()
        self.calculate_medicine_fee()
        self.calculate_total_amount()

        # Save instance
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Billing Info of Patient {self.patient.user.username}"



class HospitalBill(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='hospital_bills')
    bill_generated_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid')
    paid_on = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    accountant = models.ForeignKey(Accountant, on_delete=models.CASCADE, related_name='hospital_bills', blank=True,
                                   null=True)

    def __str__(self):
        return f"Hospital Bill for {self.patient.user.username} - Status: {self.status}"

    def mark_as_paid(self, amount , accountant):
        """Method to mark the bill as paid and update the payment details."""
        self.status = 'paid'
        self.amount_paid = amount
        self.paid_on = timezone.now()
        self.accountant = accountant
        self.save()

    def mark_as_unpaid(self):
        """Method to mark the bill as unpaid."""
        self.status = 'unpaid'
        self.amount_paid = 0.00
        self.paid_on = None
        self.save()

    def save(self, *args, **kwargs):
        """Override save to ensure the total amount is copied from the related Billing model."""
        if not self.total_amount:
            self.total_amount = self.patient.billing.total_amount  
        super().save(*args, **kwargs)
