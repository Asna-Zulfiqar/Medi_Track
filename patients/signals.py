import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from medical_records.models import MedicalRecord
from patients.models import Patient
from staff.models import Receptionist
from patients.tasks import send_patient_notification_email , send_icu_notification_email_task
from datetime import datetime, time
from wards.models import Ward, Bed


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Patient)
def notify_receptionist_on_patient_registration(sender, instance, created, **kwargs):
    if created:
        logger.info("Signal triggered for patient registration: %s", instance.user.username)

        # Get the current shift
        shift = get_current_shift()
        logger.info("Current shift: %s", shift)

        # Fetch the receptionist for the current shift
        receptionist = Receptionist.objects.filter(shift=shift).first()
        if receptionist and receptionist.user.email:

            send_patient_notification_email.delay(
                user_email=receptionist.user.email,
                receptionist_name=receptionist.user.username,
                patient_name=instance.user.username,
                patient_id=instance.id,
            )
            logger.info("Email task queued for receptionist: %s", receptionist.user.email)
        else:
            logger.warning("No receptionist found for shift: %s", shift)


def get_current_shift():
    """Determine the current shift based on the current time."""
    now = datetime.now().time()
    try:
        if time(0, 0) <= now < time(8, 0):
            return "12:00 AM - 8:00 AM"
        elif time(8, 0) <= now < time(16, 0):
            return "8:00 AM - 4:00 PM"
        else:
            return "4:00 PM - 12:00 AM"
    except Exception as e:
        logger.error("Error determining shift: %s", e)
        raise


@receiver(pre_save, sender=MedicalRecord)
def assign_bed_for_emergency_patient(sender, instance, **kwargs):
    if instance.emergency and (not instance.pk or MedicalRecord.objects.filter(pk=instance.pk, emergency=False).exists()):
        icu_ward = Ward.objects.filter(ward_type="ICU").first()
        if not icu_ward:
            raise Exception("ICU Ward does not exist.")

        # Find the current manager using the `is_within_shift` method
        ward_manager = None
        for manager in icu_ward.managers.all():
            if manager.is_within_shift():
                ward_manager = manager
                break

        if not ward_manager:
            raise Exception("No manager is currently on shift for the ICU Ward.")

        # Find an available bed in the ICU Ward
        available_bed = Bed.objects.filter(ward=icu_ward, status='free').first()
        if not available_bed:
            raise Exception("No available beds in the ICU Ward.")

        # Assign the bed to the patient and mark it as occupied
        available_bed.status = 'occupied'
        available_bed.save()

        # Update the MedicalRecord
        instance.ward_admitted_to = icu_ward
        instance.ward_admit_date = now().date()
        instance.assigned_bed = available_bed

        # Send email notification
        send_icu_notification_email_task.delay(
            manager_email=ward_manager.user.email,
            manager_name=ward_manager.user.username,
            patient_name=str(instance.patient)
        )
