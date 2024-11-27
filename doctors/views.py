from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer

class DoctorListView(ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        # Check if the user already exists in the Doctor group
        if Doctor.objects.filter(user=user).exists():
            raise ValidationError("You already have a Doctor identity.")

        serializer.save(user=user)

class DoctorDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not user.groups.filter(name="Doctor").exists():
            raise PermissionDenied("You are not authorized to view this doctor profile.")
        return Doctor.objects.get(user=user)