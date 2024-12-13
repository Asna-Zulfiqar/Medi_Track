from django.db.models.signals import post_save
from django.dispatch import receiver
from pharmacy.models import MedicineAllocation, Medicine
from pharmacy.tasks import send_medicine_allocation_emails_task, send_reorder_alert


@receiver(post_save, sender=MedicineAllocation)
def send_medicine_allocation_emails(sender, instance, created, **kwargs):
    if created:
        # Extract details from the MedicineAllocation instance
        patient = instance.patient
        pharmacy = instance.pharmacy
        medicine = instance.medicine
        quantity = instance.quantity
        medicine_name = medicine.medicine_name
        medicine_price = medicine.price
        total_amount = medicine_price * quantity

        # Call the Celery task to send emails asynchronously
        send_medicine_allocation_emails_task.delay(
            patient_id=patient.user.username,
            pharmacy_name=pharmacy.pharmacy_name,
            pharmacy_email=pharmacy.email,
            patient_email=patient.user.email,
            medicine_name=medicine_name,
            quantity=quantity,
            medicine_price=medicine_price,
            total_amount=total_amount
        )
        print(f"Email task queued for {medicine_name} purchase by {patient.user.username}")

@receiver(post_save, sender=Medicine)
def check_stock_level(sender, instance, created, **kwargs):
    if not created:
        if instance.needs_reorder():
            send_reorder_alert.delay(instance.pharmacy.email, instance.pharmacy.pharmacy_name , instance.medicine_name , instance.stock , instance.reorder_level)
