from celery import shared_task
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from billing.models import Accountant
from patients.models import Patient


@shared_task
def send_bill_email_to_patient(patient_id, pdf_content):

    # Fetch the patient instance
    patient = Patient.objects.get(pk=patient_id)

    # Email subject and message
    subject = "Your Hospital Bill from MediTrack"
    message = (
        f"Dear {patient.user.get_full_name() or patient.user.first_name},\n\n"
        "We hope this email finds you well. Attached to this message is your bill for the "
        "services provided during your visit to MediTrack Hospital.\n\n"
        "If you have any questions or concerns regarding this bill, please do not hesitate "
        "to contact our billing department at billing@meditrackhospital.com or call us at "
        "1-800-MEDI-CARE.\n\n"
        "Thank you for choosing MediTrack Hospital. We are committed to providing you with "
        "the best care and service.\n\n"
        "Kind regards,\n"
        "MediTrack Hospital Billing Team"
    )

    # Create the email message with the PDF attached
    email = EmailMessage(
        subject=subject,
        body=message,
        to=[patient.user.email],
    )

    # Attach the PDF bill
    email.attach(
        filename=f"bill_for_{patient.user.username}.pdf",
        content=pdf_content,
        mimetype='application/pdf'
    )

    # Send the email
    try:
        email.send(fail_silently=False)
        print(f"Bill successfully sent to {patient.user.email}")
    except Exception as e:
        raise RuntimeError(f"Failed to send the bill to {patient.user.email}. Error: {e}")

@shared_task
def send_bill_email_to_accountant(accountant_id):
    # Fetch the accountant instance or raise a 404 error if not found
    accountant = get_object_or_404(Accountant, pk=accountant_id)
    accountant_email = accountant.user.email

    # Validate that the accountant has a valid email address
    if not accountant_email:
        raise ValueError(
            f"The accountant with ID {accountant_id} does not have a valid email address."
        )

    # Email content
    subject = "Notification: New Bill Generated"
    body = (
        f"Dear {accountant.user.get_full_name() or 'Accountant'},\n\n"
        "This is to inform you that a new bill has been generated for a patient.\n"
        "Please review the Hospital Billing records for further details.\n\n"
        "Kind regards,\n"
        "MediTrack Hospital Billing Team"
    )
    from_email = "codingfalsafa@gmail.com"

    # Send the email
    try:
        email_message = EmailMessage(subject, body, from_email, [accountant_email])
        email_message.send(fail_silently=False)
    except Exception as e:
        raise RuntimeError(
            f"Failed to send notification email to {accountant_email}. Error: {e}"
        )