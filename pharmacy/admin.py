from django.contrib import admin
from pharmacy.models import Pharmacy, Medicine , MedicineAllocation

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['pharmacy_name', 'email', 'contact', 'user' , 'opening_hours' , 'closing_hours']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'pharmacy', 'stock', 'expiration_date', 'reorder_level']
    list_filter = ['expiration_date']

@admin.register(MedicineAllocation)
class MedicineAllocationAdmin(admin.ModelAdmin):
    list_display = ['patient' , 'pharmacy' , 'medicine' , 'quantity' , 'allocated_at']