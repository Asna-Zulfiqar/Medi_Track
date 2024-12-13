from django.urls import path
from feedback.views import FeedbackCreateView, DoctorFeedbackCreateView, ServiceFeedbackCreateView, \
    CreateStaffFeedbackView, GetUserFeedbackView

urlpatterns = [
    path('hospital/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('doctor/', DoctorFeedbackCreateView.as_view(), name='doctor_feedback_create'),
    path('service/', ServiceFeedbackCreateView.as_view(), name='service_feedback_create'),
    path('staff/', CreateStaffFeedbackView.as_view(), name='create_staff_feedback'),
    path('', GetUserFeedbackView.as_view(), name='get-user-feedback'),
]
