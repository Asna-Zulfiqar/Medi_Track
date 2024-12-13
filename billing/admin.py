from django.contrib import admin
from billing.models import Accountant, Billing, HospitalBill


class AccountantAdmin(admin.ModelAdmin):
    list_display = ('user', 'ward', 'shift_timings', 'age', 'contact', 'is_available')

class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'consultation_fee', 'bed_fee', 'surgery_fee', 'medicine_fee', 'lab_test_fee', 'total_amount', 'generated_at')

class HospitalBillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'status', 'amount_paid', 'total_amount', 'bill_generated_on', 'paid_on', 'accountant')

admin.site.register(Accountant, AccountantAdmin)
admin.site.register(Billing, BillingAdmin)
admin.site.register(HospitalBill, HospitalBillAdmin)
