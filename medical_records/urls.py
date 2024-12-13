from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from medical_records.views import MedicalRecordDetailView, MedicinePrescriptionListCreateView, \
    MedicinePrescriptionDetailView, LabPrescriptionListCreateView, LabPrescriptionDetailView

urlpatterns = [
    path('', MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('medicine_prescriptions/', MedicinePrescriptionListCreateView.as_view(), name='medicine-prescription-list-create'),
    path('medicine_prescriptions/details/' ,  MedicinePrescriptionDetailView.as_view() , name = 'medicine-prescription-detail'),
    path('lab_prescriptions/', LabPrescriptionListCreateView.as_view(), name='lab_prescription-list-create'),
    path('lab_pescriptions/details/' , LabPrescriptionDetailView.as_view() , name = 'lab-prescription-detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
