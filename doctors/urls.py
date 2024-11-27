from django.urls import path
from doctors.views import DoctorListView, DoctorDetailView

urlpatterns = [
    path('list/', DoctorListView.as_view(), name='doctor-list'),
    path('detail/', DoctorDetailView.as_view(), name='doctor-detail'),
]