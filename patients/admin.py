from django.contrib import admin
from patients.models import Patient, Condition, Allergy, Surgery, MedicalHistory


admin.site.register(Patient)
admin.site.register(Condition)
admin.site.register(Allergy)
admin.site.register(Surgery)
admin.site.register(MedicalHistory)
