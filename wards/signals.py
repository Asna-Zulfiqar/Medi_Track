from django.db.models.signals import post_save
from django.dispatch import receiver
from wards.models import Ward


# Signal to create beds Automatically when a ward is created
@receiver(post_save, sender=Ward)
def create_beds(sender, instance, created, **kwargs):
    if created:  # Only create beds when a new ward is created
        instance.refresh_from_db()
        instance.create_beds()
