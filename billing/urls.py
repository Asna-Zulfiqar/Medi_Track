from django.urls import path
from billing.views import BillRequestView, HospitalBillListView, HospitalBillBatchUpdateView

urlpatterns = [
    path("request/", BillRequestView.as_view(), name="request_bill_api"),
    path('hospital_bills/', HospitalBillListView.as_view(), name='hospital-bill-list'),
    path('hospital_bills/batch_update/', HospitalBillBatchUpdateView.as_view(), name='hospital-bill-batch-update'),
]
