from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from appointments.models import Appointment


@shared_task
def send_appointment_email(appointment_id, status):

    from appointments.models import Appointment # Local Import to avoid circular import
    appointment = Appointment.objects.get(id=appointment_id)
    subject = f"Appointment {status.capitalize()} - Dr. {appointment.doctor.user.username}"

    # Message body for the patient
    message_patient = f"""
    Dear {appointment.patient.user.username},

    We would like to inform you about the status of your appointment with Dr. {appointment.doctor.user.username}. 

    Appointment Details:
    - Doctor: Dr. {appointment.doctor.user.username}
    - Date and Time: {appointment.appointment_date}
    - Status: {status.capitalize()}


    We kindly request you to review the appointment details. If you have any questions or if any changes are required, please do not hesitate to contact us.

    Best regards,
    The MediTrack Team
    """

    # Sending email to the patient
    send_mail(
        subject=subject,
        message=message_patient,
        from_email="codingfalsafa@gmail.com",
        recipient_list=[appointment.patient.user.email],
        fail_silently=False,
    )

    # Message body for the doctor
    message_doctor = f"""
    Dear Dr. {appointment.doctor.user.username},

    This is a notification regarding your upcoming appointment with {appointment.patient.user.username}.

    Appointment Details:
    - Patient: {appointment.patient.user.username}
    - Date and Time: {appointment.appointment_date.strftime('%A, %B %d, %Y at %I:%M %p')}
    - Status: {status.capitalize()}


    Please ensure to be available at the scheduled time. If there are any updates or changes, kindly let us know.

    Best regards,
    The MediTrack Team
    """

    # Sending email to the doctor
    send_mail(
        subject=subject,
        message=message_doctor,
        from_email="codingfalsafa@gmail.com",
        recipient_list=[appointment.doctor.user.email],
        fail_silently=False,
    )

@shared_task
def send_appointment_reminder(appointment_id):
    try:
        # Fetch the appointment details
        appointment = Appointment.objects.get(id=appointment_id)

        # Ensure appointment_date is aware
        appointment_date = appointment.appointment_date
        if appointment_date.tzinfo is None:
            appointment_date = timezone.make_aware(appointment_date, timezone.get_current_timezone())

        # Calculate the time 1 hour before the appointment
        reminder_time = appointment_date - timedelta(hours=1)
        # Check if it's time to send the reminder (ensure timezone.now() is also timezone-aware)
        if timezone.now() >= reminder_time:
            # Compose the reminder email
            subject = f"Reminder: Your appointment with Dr. {appointment.doctor.user.username}"
            message = f"Dear {appointment.patient.user.username},\n\nThis is a reminder that you have an appointment with Dr. {appointment.doctor.user.username} on {appointment.appointment_date}.\n\nPlease be on time.\n\nBest regards,\nYour Healthcare Team"
            recipient_list = [appointment.patient.user.email]

            # Send email to the patient
            send_mail(subject, message, 'codingfalsafa@gmail.com', recipient_list)

            subject = f"Reminder: Upcoming appointment with {appointment.patient.user.username}"
            message = f"Dear Dr. {appointment.doctor.user.username},\n\nThis is a reminder that you have an appointment with {appointment.patient.user.username} on {appointment.appointment_date}.\n\nBest regards,\nYour Healthcare Team"
            recipient_list = [appointment.doctor.user.email]

            # Send email to the doctor
            send_mail(subject, message, 'codingfalsafa@gmail.com', recipient_list)

    except Appointment.DoesNotExist:
        # Log or handle the case where the appointment is missing
        print(f"Appointment with ID {appointment_id} does not exist.")