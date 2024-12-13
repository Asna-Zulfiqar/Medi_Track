from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from wards.models import Ward, WardManager
from wards.serializers import WardSerializer, WardManagerSerializer
from staff.permissions import IsWardManagerGroup

class WardDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = WardSerializer
    permission_classes = [IsAuthenticated , IsWardManagerGroup]

    def get_queryset(self):
        user = self.request.user
        return Ward.objects.filter(managers__user=user)

    def get_object(self):
        user = self.request.user
        # Get the ward associated with the current logged-in user
        ward = Ward.objects.filter(managers__user=user).first()

        if ward is None:
            raise NotFound('Ward not found for this user')

        return ward

    def update(self, request, *args, **kwargs):
        # Get the ward instance
        instance = self.get_object()

        # Update the ward details
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update bed statuses if provided
        bed_updates = request.data.get('beds')
        if bed_updates:
            for bed_data in bed_updates:
                bed_id = bed_data.get('id')
                if not bed_id:
                    continue
                # Get the bed object using the provided ID
                bed = get_object_or_404(instance.beds, id=bed_id)
                # Update the status of the bed if provided
                bed.status = bed_data.get('status', bed.status)  # Default to current status if not provided
                bed.save()

        return Response(serializer.data)


class WardManagerListCreateView(ListCreateAPIView):
    queryset = WardManager.objects.all()
    serializer_class = WardManagerSerializer
    permission_classes = [IsAuthenticated , IsWardManagerGroup]

    def perform_create(self, serializer):
        if WardManager.objects.filter(user=self.request.user).exists():
            raise ValidationError(f"You are already assigned to a ward with a shift.")
        serializer.save(user=self.request.user)

class WardManagerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = WardManagerSerializer
    permission_classes = [IsAuthenticated , IsWardManagerGroup]

    def get_object(self):
        user = self.request.user
        return WardManager.objects.get(user=user)