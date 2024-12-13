from django.urls import path
from pharmacy.views import PharmacyCreateView, PharmacyDetailView, MedicineCreateView, MedicineAllocationView

urlpatterns = [
    path('create/', PharmacyCreateView.as_view(), name='pharmacy-create'),
    path('detail/', PharmacyDetailView.as_view(), name='pharmacy-detail'),
    path('medicine/create/', MedicineCreateView.as_view(), name='medicine-create'),
    path('allocate_medicine/', MedicineAllocationView.as_view(), name='allocate-medicine'),
]
