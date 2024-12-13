# admin.py
from django.contrib import admin
from .models import Ward, Bed, WardManager

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_type', 'capacity')

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('id', 'ward', 'status', 'created_at')

@admin.register(WardManager)
class WardManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'ward', 'shift')