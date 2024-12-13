from rest_framework.exceptions import  ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from patients.models import Patient
from pharmacy.models import Pharmacy
from pharmacy.serializers import PharmacySerializer, MedicineSerializer, MedicineAllocationSerializer
from staff.permissions import IsPharmacistGroup, IsPatientGroup


class PharmacyCreateView(CreateAPIView):
    serializer_class = PharmacySerializer
    permission_classes = [IsAuthenticated , IsPharmacistGroup]

    def get_queryset(self):
        return Pharmacy.objects.all()

    def perform_create(self, serializer):

        if Pharmacy.objects.filter(user=self.request.user).exists():
            raise ValidationError("You already have a Pharmacy")

        serializer.save(user=self.request.user)

class PharmacyDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PharmacySerializer
    permission_classes = [IsAuthenticated , IsPharmacistGroup]

    def get_object(self):
        user = self.request.user
        return Pharmacy.objects.get(user=user)


class MedicineCreateView(CreateAPIView):
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated , IsPharmacistGroup]

    def perform_create(self, serializer):
        pharmacy = Pharmacy.objects.get(user=self.request.user)
        serializer.save(pharmacy=pharmacy)


class MedicineAllocationView(CreateAPIView):
    serializer_class = MedicineAllocationSerializer
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def perform_create(self, serializer):
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(patient = patient)

