from django.contrib import admin
from doctors.models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'contact', 'experience')

admin.site.register(Doctor, DoctorAdmin)
