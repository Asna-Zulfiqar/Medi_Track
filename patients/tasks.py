from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

@shared_task
def send_patient_notification_email(user_email, receptionist_name , patient_name, patient_id):
    """
        Send  email to the receptionist to check for emergency patients.
    """
    base_url = settings.SITE_URL
    patient_medical_record_url = f"{base_url}{reverse('medical_record_detail')}?patient_id={patient_id}"

    subject = "New Patient Registration Alert"
    message = f"""
    Dear Receptionist {receptionist_name},

    A new patient has registered at the hospital. Please address the patient immediately.

    Patient Name: {patient_name}
    Patient Medical Record Portal: {patient_medical_record_url}

    Regards,
    Medi Track - Hospital Management System
    """
    send_mail(
        subject=subject,
        message=message,
        from_email="codingfalsafa@gmail.com",
        recipient_list=[user_email],
        fail_silently=False,
    )

@shared_task
def send_icu_notification_email_task(manager_email, manager_name , patient_name):
    """
    Send  email notification to the ICU ward manager.
    """
    subject = f"Emergency Patient Assigned to ICU"
    message = f"""
    Dear Ward Manager {manager_name},

    An emergency patient named {patient_name} has been assigned to the ICU.
    Please ensure the necessary preparations are made.

    Regards,
    Hospital Management System
    """
    send_mail(
        subject=subject,
        message=message,
        from_email="codingfalsafa@gmail.com",
        recipient_list=[manager_email],
        fail_silently=False,
    )