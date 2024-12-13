from rest_framework.exceptions import  ValidationError
from rest_framework.generics import  RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from staff.permissions import IsDoctorGroup
from patients.models import Patient
from patients.serializers import PatientSerializer


class DoctorProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated , IsDoctorGroup]

    def get_object(self):
        user = self.request.user
        return Doctor.objects.get(user=user)

class DoctorPatientDetailView(APIView):
    permission_classes = [IsAuthenticated , IsDoctorGroup]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Get patient by ID  from query parameters
        patient_id = request.query_params.get("id")  # e.g  /doctor/patient_detail/?id=5

        if not patient_id:
            raise ValidationError("Please provide  'id'  to fetch patient details.")

        # Fetch the patient
        try:
            if patient_id:
                patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise ValidationError("No matching patient found.")

        patient_data = PatientSerializer(patient).data
        response_data = {
            "patient": patient_data,
        }

        return Response(response_data, status=200)