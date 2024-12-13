from django.contrib import admin
from laboratory.models import Laboratory, Test , LabTestAllocation

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('lab_name', 'user', 'contact', 'email', 'opening_hours', 'closing_hours', 'is_open')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'laboratory', 'price', 'duration')

@admin.register(LabTestAllocation)
class LabTestAllocationAdmin(admin.ModelAdmin):
    list_display = ['patient' , 'prescription' , 'laboratory' , 'allocated_on' , 'status']

