from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_medicine_allocation_emails_task(patient_id, pharmacy_name, pharmacy_email, patient_email, medicine_name, quantity, medicine_price, total_amount):
    # Email content for the pharmacy
    pharmacy_subject = f"New Medicine Purchase from {patient_id}"
    pharmacy_message = f"Dear {pharmacy_name} Team,\n\n" \
                       f"A patient has purchased the following medicine from your pharmacy:\n\n" \
                       f"Patient ID: {patient_id}\n" \
                       f"Medicine: {medicine_name}\n" \
                       f"Quantity: {quantity}\n" \
                       f"Price per Unit: {medicine_price}\n" \
                       f"Total Amount: {total_amount}\n\n" \
                       f"Pharmacy: {pharmacy_name}\n" \
                       f"Please process the order and ensure delivery.\n\n" \
                       f"Best regards,\n" \
                       f"The Healthcare System"

    send_mail(
        pharmacy_subject,
        pharmacy_message,
        settings.DEFAULT_FROM_EMAIL,
        [pharmacy_email],
        fail_silently=False,
    )

    # Email content for the patient
    patient_subject = "Your Medicine Purchase Details"
    patient_message = f"Dear {patient_id},\n\n" \
                      f"Thank you for your purchase. Here are the details of the medicine you bought:\n\n" \
                      f"Medicine Name: {medicine_name}\n" \
                      f"Quantity: {quantity}\n" \
                      f"Price per Unit: {medicine_price}\n" \
                      f"Total Amount: {total_amount}\n\n" \
                      f"Pharmacy Name: {pharmacy_name}\n" \
                      f"Your purchase will be processed shortly. If you have any questions, please contact the pharmacy.\n\n" \
                      f"Best regards,\n" \
                      f"Medi Track Hospital Management"

    send_mail(
        patient_subject,
        patient_message,
        settings.DEFAULT_FROM_EMAIL,
        [patient_email],
        fail_silently=False,
    )


@shared_task
def send_reorder_alert(pharmacy_email, pharmacy_name, medicine_name, stock, reorder_level):
    subject = f'Action Required: Reorder Alert for {medicine_name}'

    message = f"""
    Dear Pharmacy Team at {pharmacy_name},

    This is a reminder that the stock of {medicine_name} in your pharmacy has fallen below the critical reorder level.

    Medicine: {medicine_name}
    Current Stock: {stock}
    Reorder Level: {reorder_level}

    Please take immediate action to reorder the medicine and ensure that you maintain sufficient stock levels to avoid shortages.

    Should you need assistance or wish to place an order, please contact your supplier or reach out to our customer support team.

    Thank you for your attention to this matter.

    Best regards,
    Medi Track Hospital Management
    """

    # Sending the email
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[pharmacy_email],
    )
