from django.contrib import admin
from appointments.models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'created_at')

admin.site.register(Appointment, AppointmentAdmin)

