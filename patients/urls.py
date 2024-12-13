from django.urls import path
from patients.views import MedicalHistoryListCreateView,  PatientProfileView

urlpatterns = [
    path('medical_history/', MedicalHistoryListCreateView.as_view(), name='medical_history_list_create'),
    path('profile/' , PatientProfileView.as_view() , name='patient_details'),
]