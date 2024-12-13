from rest_framework import serializers
from appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'appointment_date', 'status', 'notes']

    def validate(self, data):
        """
        Custom validation for checking doctor availability.
        """
        appointment_instance = self.instance
        doctor = data.get('doctor')
        appointment_date = data.get('appointment_date')
        status = data.get('status')

        # No need to check availability if the appointment is cancelled
        if status == 'cancelled':
            return data

        # Validate if the doctor is available for the given date
        if appointment_date and doctor:
            # If updating, exclude the current appointment instance from the query
            conflicting_appointments = Appointment.objects.filter(
                doctor=doctor, appointment_date=appointment_date
            )
            if appointment_instance:
                conflicting_appointments = conflicting_appointments.exclude(id=appointment_instance.id)

            if conflicting_appointments.exists():
                raise serializers.ValidationError("The doctor is not available at the selected time.")

        return data
