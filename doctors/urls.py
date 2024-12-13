from django.urls import path
from doctors.views import DoctorProfileView, DoctorPatientDetailView

urlpatterns = [
    path('profile/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('patient_detail/', DoctorPatientDetailView.as_view(), name='doctor-patient-detail'),
]