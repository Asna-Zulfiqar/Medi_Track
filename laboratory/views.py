from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from laboratory.models import Laboratory
from laboratory.serializers import LabTestAllocationSerializer, LaboratorySerializer, TestSerializer, \
    TestResultSerializer
from laboratory.tasks import send_lab_test_emails , send_test_result_email_to_patient
from medical_records.models import  TestResult
from patients.models import Patient
from staff.permissions import IsLabTechnicianGroup, IsPatientGroup


class LaboratoryCreateView(CreateAPIView):
    serializer_class = LaboratorySerializer
    permission_classes = [IsAuthenticated , IsLabTechnicianGroup]

    def get_queryset(self):
        return Laboratory.objects.all()

    def perform_create(self, serializer):

        if Laboratory.objects.filter(user=self.request.user).exists():
            raise ValidationError("You already have a Laboratory")

        serializer.save(user=self.request.user)

class LaboratoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = LaboratorySerializer
    permission_classes = [IsAuthenticated , IsLabTechnicianGroup]

    def get_object(self):
        user = self.request.user
        return Laboratory.objects.get(user=user)


class TestCreateView(CreateAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated , IsLabTechnicianGroup]

    def perform_create(self, serializer):
        laboratory = Laboratory.objects.get(user=self.request.user)
        serializer.save(laboratory=laboratory)



class LabTestAllocationView(CreateAPIView):
    serializer_class = LabTestAllocationSerializer
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def perform_create(self, serializer):
        try:
            patient = self.request.user.patient_profile
        except Patient.DoesNotExist:
            raise ValidationError("The current user is not associated with a patient profile.")

        lab_test_allocation = serializer.save(patient=patient)

        # Send the lab test emails after saving the allocation
        if lab_test_allocation:
            send_lab_test_emails.delay(
                lab_test_allocation.id,
            )

        return Response(
            {"message": "Lab test allocated successfully."},
            status=status.HTTP_201_CREATED
        )


class TestResultUploadView(CreateAPIView):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated , IsLabTechnicianGroup]

    def perform_create(self, serializer):
        test_result = serializer.save()

        # Send email asynchronously using Celery
        send_test_result_email_to_patient.delay(test_result.id)