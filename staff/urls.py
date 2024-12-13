from django.urls import path
from staff.views import  NurseDetailView, \
    SecurityGuardDetailView, ReceptionistDetailView, SweeperDetailView

urlpatterns = [
    # Receptionist
    path('receptionists/', ReceptionistDetailView.as_view(), name='receptionist-detail'),

    # Security Guard
    path('security_guards/', SecurityGuardDetailView.as_view(), name='security-guard-detail'),

    # Sweeper
    path('sweepers/', SweeperDetailView.as_view(), name='sweeper-detail'),

    # Nurse
    path('nurses/', NurseDetailView.as_view(), name='nurse-detail'),
]
