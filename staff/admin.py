from django.contrib import admin
from staff.models import SecurityGuard, Sweeper, Receptionist , Nurse

class SecurityGuardAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'shift_timings', 'is_available', 'ward')

admin.site.register(SecurityGuard, SecurityGuardAdmin)


class SweeperAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'shift_timings', 'is_available', 'ward')

admin.site.register(Sweeper, SweeperAdmin)

@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ('user', 'shift', 'contact_number')

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'shift_timings', 'is_available', 'ward')