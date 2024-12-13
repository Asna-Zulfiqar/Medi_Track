from django.contrib import admin
from .models import DeviceToken

class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')


admin.site.register(DeviceToken, DeviceTokenAdmin)
