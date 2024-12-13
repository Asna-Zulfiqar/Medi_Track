from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from doctors.serializers import DoctorSerializer
from doctors.models import Doctor
from staff.permissions import IsPatientGroup
from appointments.tasks import send_appointment_email

class AppointmentCreateView(ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def get(self, request, *args, **kwargs):
        """
        Fetch the list of doctors for the patient to choose from when setting up an appointment.
        """
        doctors = Doctor.objects.all()
        doctor_data = DoctorSerializer(doctors, many=True).data
        return Response({"doctors": doctor_data})

    def perform_create(self, serializer):
        user = self.request.user

        # Check if the logged-in user is a patient
        try:
            patient = user.patient_profile
        except AttributeError:
            raise ValidationError("The logged-in user is not associated with a patient profile.")

            # Save the appointment with the associated patient
        appointment = serializer.save(patient=patient)

        # Trigger email only if appointment is scheduled
        if appointment.status == 'scheduled':
            print(f"Triggering email for new appointment {appointment.id}")
            send_appointment_email.delay(appointment.id, 'Scheduled')

class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def get(self, request):
        try:
            patient = request.user.patient_profile
        except AttributeError:
            return Response({"error": "No Patient Found with this id."}, status=status.HTTP_403_FORBIDDEN)

        appointments = Appointment.objects.filter(patient=patient)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update a specific appointment for the logged-in patient.
        """
        try:
            patient = request.user.patient_profile
        except AttributeError:
            return Response(
                {"error": "The logged-in user is not a patient."}, status=status.HTTP_403_FORBIDDEN
            )

        # Extract the appointment ID from the request body
        appointment_id = request.data.get('id')
        if not appointment_id:
            return Response({"error": "Appointment ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the specific appointment by ID and ensure it's linked to the logged-in patient
            appointment = Appointment.objects.get(id=appointment_id, patient=patient)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data and validate
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            updated_appointment = serializer.save()

            # Trigger email after update if the status has changed (e.g., cancelled or rescheduled)
            if updated_appointment.status == 'cancelled':
                print(f"Triggering email for cancelled appointment {updated_appointment.id}")
                send_appointment_email.delay(updated_appointment.id, 'cancelled')
            elif updated_appointment.status == 'rescheduled':
                print(f"Triggering email for rescheduled appointment {updated_appointment.id}")
                send_appointment_email.delay(updated_appointment.id, 'rescheduled')

            return Response(
                {"message": "Appointment updated successfully.", "appointments": [serializer.data]},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

