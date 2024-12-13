from django.urls import path
from appointments.views import AppointmentCreateView, AppointmentDetailView


urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='appointments'),
    path('detail/', AppointmentDetailView.as_view(), name='appointment_detail'),

]
