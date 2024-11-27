from django.urls import path
from patients.views import MedicalHistoryListCreateView, PatientCreateView, PatientDetailView

urlpatterns = [
    path('profile/' , PatientCreateView.as_view() , name='patient_create'),
    path('medical-history/', MedicalHistoryListCreateView.as_view(), name='medical-history-list-create'),
    path('details/' , PatientDetailView.as_view() , name='patient_details'),
]