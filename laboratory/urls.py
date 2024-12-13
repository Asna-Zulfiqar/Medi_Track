from django.urls import path
from laboratory.views import (
    LaboratoryCreateView,
    LaboratoryDetailView,
    LabTestAllocationView, TestCreateView, TestResultUploadView,
)

urlpatterns = [
    path('create/', LaboratoryCreateView.as_view(), name='lab_prescription_list_create'),
    path('detail/', LaboratoryDetailView.as_view(), name='lab_prescription_detail'),
    path('test_create/' , TestCreateView.as_view(), name='lab_prescription_test_create'),
    path('allocate_lab_test/', LabTestAllocationView.as_view(), name='lab_test_allocate'),
    path('upload_test_result/', TestResultUploadView.as_view(), name='upload_test_result'),
]
