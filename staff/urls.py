from django.urls import path
from staff.views import NurseDetailView, \
    SecurityGuardDetailView, ReceptionistDetailView, SweeperDetailView, AccountantDetailView

urlpatterns = [
    path('receptionists/', ReceptionistDetailView.as_view(), name='receptionist-detail'),
    path('security_guards/', SecurityGuardDetailView.as_view(), name='security-guard-detail'),
    path('sweepers/', SweeperDetailView.as_view(), name='sweeper-detail'),
    path('nurses/', NurseDetailView.as_view(), name='nurse-detail'),
    path('accountants/', AccountantDetailView.as_view(), name='accountant-detail'),
]
