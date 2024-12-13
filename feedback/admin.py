from django.contrib import admin
from feedback.models import Feedback, DoctorFeedback, ServiceFeedback, StaffFeedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['patient' , 'rating' , 'created_at']

@admin.register(DoctorFeedback)
class DoctorFeedbackAdmin(admin.ModelAdmin):
    list_display = ['patient' , 'doctor' , 'rating' , 'created_at']

@admin.register(ServiceFeedback)
class ServiceFeedbackAdmin(admin.ModelAdmin):
    list_display = ['patient' , 'service' , 'rating' , 'created_at']

@admin.register(StaffFeedback)
class StaffFeedbackAdmin(admin.ModelAdmin):
    list_display = ['patient' , 'staff' , 'rating' , 'created_at']