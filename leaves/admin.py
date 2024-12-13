from django.contrib import admin
from leaves.models import Leave

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'status', 'created_at']

