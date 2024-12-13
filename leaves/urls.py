from django.urls import path
from leaves.views import LeaveApplicationView, LeaveDetailView

urlpatterns = [
    path('apply/', LeaveApplicationView.as_view(), name='apply-leave'),
    path('update/' , LeaveDetailView.as_view(), name='update-leave'),
]
