from django.contrib.auth.models import User
from django.db import models


class DeviceToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="device_token")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Device Token"
