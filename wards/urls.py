from django.urls import path
from wards.views import ( WardDetailView,
                         WardManagerListCreateView, WardManagerDetailView)


urlpatterns = [
    path('details/', WardDetailView.as_view(), name='ward-detail'),
    path('managers/', WardManagerListCreateView.as_view(), name='ward-manager-list-create'),
    path('managers/detail/', WardManagerDetailView.as_view(), name='ward-manager-detail'),
]
