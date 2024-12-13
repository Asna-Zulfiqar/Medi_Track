from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from appointments.models import Appointment
from appointments.tasks import send_appointment_reminder

@receiver(pre_save, sender=Appointment)
def cache_original_date(sender, instance, **kwargs):
    """
    Cache the original appointment date before saving the instance.
    """
    if instance.pk:
        try:
            # Retrieve the original instance to cache its date
            instance._original_date = Appointment.objects.get(pk=instance.pk).appointment_date
        except Appointment.DoesNotExist:
            instance._original_date = None
    else:
        instance._original_date = None

@receiver(post_save, sender=Appointment)
def schedule_appointment_reminder(sender, instance, created, **kwargs):
    """
    Schedule or reschedule the reminder email for an appointment.
    """
    # Ensure the date is timezone-aware
    appointment_date = instance.appointment_date
    if appointment_date.tzinfo is None:  # If naive
        appointment_date = timezone.make_aware(appointment_date, timezone.get_current_timezone())

    # Calculate the time for the reminder
    reminder_time = appointment_date - timedelta(hours=1)

    if created:
        # Schedule the reminder for a newly created appointment
        send_appointment_reminder.apply_async((instance.id,), eta=reminder_time)
    else:
        # Check if the date was changed (rescheduled)
        if instance._original_date and instance._original_date != instance.appointment_date:
            send_appointment_reminder.apply_async((instance.id,), eta=reminder_time)
