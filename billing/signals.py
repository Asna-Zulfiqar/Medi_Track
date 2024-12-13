from django.db.models.signals import post_save
from django.dispatch import receiver
from laboratory.models import LabTestAllocation
from pharmacy.models import MedicineAllocation
from billing.models import Billing
from decimal import Decimal

@receiver(post_save, sender=MedicineAllocation)
def handle_medicine_billing(sender, instance, created, **kwargs):
    if created and instance.medicine and instance.quantity:
        try:
            from decimal import Decimal

            # Convert all values to Decimal
            medicine_price = Decimal(str(instance.medicine.price))
            quantity = Decimal(str(instance.quantity))
            amount = Decimal(str(medicine_price)) * Decimal(str(quantity))

            # Fetch or create Billing instance early
            billing, _ = Billing.objects.get_or_create(patient=instance.patient)

            # Initialize fields to Decimal
            billing.medicine_fee = Decimal(str(billing.medicine_fee or 0))
            billing.consultation_fee = Decimal(str(billing.consultation_fee or 0))
            billing.bed_fee = Decimal(str(billing.bed_fee or 0))
            billing.surgery_fee = Decimal(str(billing.surgery_fee or 0))
            billing.lab_test_fee = Decimal(str(billing.lab_test_fee or 0))
            billing.discount = Decimal(str(billing.discount or 0))


            # Safely accumulate medicine fee
            billing.medicine_fee += amount

            # Recalculate total amount
            billing.total_amount = (
                billing.consultation_fee +
                billing.bed_fee +
                billing.surgery_fee +
                billing.medicine_fee +
                billing.lab_test_fee -
                billing.discount
            )
            billing.save()

            print(f"Updated billing for {instance.patient.user.username}: added {amount} to medicine fee.")

        except Exception as e:
            print(f"Error handling medicine billing: {e}")


@receiver(post_save, sender=LabTestAllocation)
def handle_lab_test_billing(sender, instance, created, **kwargs):
    if created:
        try:
            # Get the billing instance for the patient
            billing, created = Billing.objects.get_or_create(patient=instance.patient)

            # Update lab test fee by summing up the price of all the allocated lab tests for the patient
            lab_test_allocations = LabTestAllocation.objects.filter(patient=instance.patient)

            # Recalculate lab test fee by summing the price of all tests
            total_lab_test_fee = sum(Decimal(allocation.prescription.test.price) for allocation in lab_test_allocations)

            # Update the billing instance's lab_test_fee
            billing.lab_test_fee = total_lab_test_fee
            print(billing.lab_test_fee)

            # Recalculate total amount
            billing.calculate_total_amount()

            # Save the updated billing instance
            billing.save()

            print(f"Lab test fee updated for patient {instance.patient}. New lab test fee: {billing.lab_test_fee}")
        except Exception as e:
            print(f"Error handling lab test billing: {e}")
