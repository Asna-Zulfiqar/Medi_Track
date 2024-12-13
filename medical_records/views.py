from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from medical_records.models import MedicalRecord, MedicinePrescription, LabPrescription
from patients.models import Patient
from medical_records.serializers import MedicalRecordSerializer, MedicinePrescriptionSerializer, \
    LabPrescriptionSerializer
from staff.permissions import CanViewMedicalRecord , IsDoctorGroup
from medical_records.tasks import send_prescription_email_to_patient

class MedicalRecordDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated , CanViewMedicalRecord]

    def get_object(self):
        user = self.request.user
        patient_id = self.request.query_params.get("patient_id")

        # If a patient_id is provided, fetch the medical record for that patient
        if patient_id:
            try:
                medical_record = MedicalRecord.objects.get(patient__id=patient_id)
            except MedicalRecord.DoesNotExist:
                # Create a new medical record if it does not exist
                patient = Patient.objects.get(id=patient_id)
                medical_record = MedicalRecord.objects.create(patient=patient)
                medical_record.save()

            self.check_object_permissions(self.request, medical_record)
            return medical_record

        # If no patient_id is provided, check if the user is a patient and try to access their record
        if user.groups.filter(name="Patient").exists():
            try:
                medical_record = MedicalRecord.objects.get(patient__user=user)
            except MedicalRecord.DoesNotExist:
                # Create a new medical record if it does not exist for the logged-in patient
                patient = user.patient
                medical_record = MedicalRecord.objects.create(patient=patient)
                medical_record.save()

            self.check_object_permissions(self.request, medical_record)
            return medical_record

        # Raise an exception if the user doesn't have access
        raise PermissionDenied("You are not authorized to access this medical record.")

class MedicinePrescriptionListCreateView(ListCreateAPIView):
    queryset = MedicinePrescription.objects.all()
    serializer_class = MedicinePrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctorGroup]

    def get_queryset(self):
        return self.queryset.filter(prescribed_by=self.request.user.doctor_profile)

    def perform_create(self, serializer):
        prescription = serializer.save(prescribed_by=self.request.user.doctor_profile)

        patient = prescription.patient

        if patient:
            # Trigger the email task
            send_prescription_email_to_patient.delay(
                'Medicine' ,prescription.id, patient.id, action="created"
            )

class MedicinePrescriptionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsDoctorGroup]

    def get(self, request):
        """
        Retrieve all medicine prescriptions linked to the logged-in doctor.
        """
        try:
            # Retrieve the Doctor instance linked to the logged-in user
            doctor = request.user.doctor_profile
        except AttributeError:
            return Response(
                {"error": "You are not registered as a doctor."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Filter prescriptions by the logged-in doctor
        prescriptions = MedicinePrescription.objects.filter(prescribed_by=doctor)
        serializer = MedicinePrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update a specific prescription for the logged-in doctor.
        """
        # Extract prescription ID from the request body
        prescription_id = request.data.get("id")
        if not prescription_id:
            return Response(
                {"error": "Prescription ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            doctor = request.user.doctor_profile

            prescription = MedicinePrescription.objects.get(
                id=prescription_id,
                prescribed_by=doctor,
            )
        except MedicinePrescription.DoesNotExist:
            return Response(
                {"error": "Prescription not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize and validate the data
        serializer = MedicinePrescriptionSerializer(
            prescription, data=request.data, partial=True
        )
        if serializer.is_valid():
            updated_prescription = serializer.save()

            # Trigger email notifications
            patient = updated_prescription.patient
            if patient:
                send_prescription_email_to_patient.delay(
                    'Medicine',
                    prescription_id=updated_prescription.id,
                    patient_id=patient.id,
                    action="updated",
                )

            return Response(
                {"message": "Prescription updated successfully.", "prescription": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LabPrescriptionListCreateView(ListCreateAPIView):
    queryset = LabPrescription.objects.all()
    serializer_class = LabPrescriptionSerializer
    permission_classes = [IsAuthenticated , IsDoctorGroup]  # Add other permission classes like IsDoctorGroup if needed

    def get_queryset(self):
        """
        Filter the lab prescriptions for the logged-in doctor
        """
        return self.queryset.filter(prescribed_by=self.request.user.doctor_profile)

    def perform_create(self, serializer):
        """
        Save the lab prescription and trigger email notifications
        """
        prescription = serializer.save(prescribed_by=self.request.user.doctor_profile)

        patient = prescription.patient

        if patient:
            # Trigger the email task to notify the patient and pharmacy
            send_prescription_email_to_patient.delay(
                'Lab' ,prescription.id, patient.id, action="created"
            )

class LabPrescriptionDetailView(APIView):
    """
    Retrieve, update, or delete lab prescriptions linked to the logged-in doctor.
    """
    permission_classes = [IsAuthenticated , IsDoctorGroup]

    def get(self, request):
        try:
            # Retrieve the Doctor instance linked to the logged-in user
            doctor = request.user.doctor_profile
        except AttributeError:
            return Response(
                {"error": "You are not registered as a doctor."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Filter prescriptions by the logged-in doctor
        prescriptions = LabPrescription.objects.filter(prescribed_by=doctor)
        serializer = LabPrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update a specific lab prescription for the logged-in doctor.
        """
        # Extract prescription ID from the request body
        prescription_id = request.data.get("id")
        if not prescription_id:
            return Response(
                {"error": "Prescription ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            doctor = request.user.doctor_profile

            prescription = LabPrescription.objects.get(
                id=prescription_id,
                prescribed_by=doctor,
            )
        except LabPrescription.DoesNotExist:
            return Response(
                {"error": "Prescription not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize and validate the data
        serializer = LabPrescriptionSerializer(
            prescription, data=request.data, partial=True
        )
        if serializer.is_valid():
            updated_prescription = serializer.save()

            # Trigger email notifications
            patient = updated_prescription.patient
            if patient:
                send_prescription_email_to_patient.delay(
                    'Lab',
                    prescription_id=updated_prescription.id,
                    patient_id=patient.id,
                    action="updated",
                )

            return Response(
                {"message": "Prescription updated successfully.", "prescription": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)