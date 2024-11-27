from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from patients.serializers import PatientSerializer , MedicalHistorySerializer
from patients.models import MedicalHistory, Patient, Surgery, Allergy , Condition


class PatientCreateView(CreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.all()

    def perform_create(self, serializer):
        # Assign the logged-in user as the user for the Patient instance
        user = self.request.user
        if Patient.objects.filter(user=user).exists():
            raise ValidationError("You already have a Patient identity.")
        serializer.save(user=user)

class MedicalHistoryListCreateView(ListCreateAPIView):
    serializer_class = MedicalHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the medical histories for the logged-in user's patient
        return MedicalHistory.objects.filter(patient__user=self.request.user)

    def perform_create(self, serializer):
        patient = Patient.objects.get(user=self.request.user)
        if MedicalHistory.objects.filter(patient=patient).exists():
            raise ValidationError("This Patient Already has a Medical History Record.")

        # Automatically assign the currently logged-in user as the patient
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(patient=patient)

class PatientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not user.groups.filter(name="Patient").exists():
            raise PermissionDenied("You are not authorized to view this Patient profile.")
        return Patient.objects.get(user=user)

    def perform_update(self, serializer):
        # Update the patient profile
        patient = serializer.save()

        # Handle medical history update
        medical_history_data = self.request.data.get('medical_history', [])
        if isinstance(medical_history_data, list):
            for history_data in medical_history_data:
                conditions_data = history_data.get('conditions', [])
                allergies_data = history_data.get('allergies', [])
                surgeries_data = history_data.get('surgeries', [])

                # Get or create the medical history for the patient
                medical_history, _ = MedicalHistory.objects.get_or_create(patient=patient)

                # Update conditions
                medical_history.conditions.clear()
                for condition_data in conditions_data:
                    condition, _ = Condition.objects.get_or_create(**condition_data)
                    medical_history.conditions.add(condition)

                # Update allergies
                medical_history.allergies.clear()
                for allergy_data in allergies_data:
                    allergy, _ = Allergy.objects.get_or_create(**allergy_data)
                    medical_history.allergies.add(allergy)

                # Update surgeries
                medical_history.surgeries.clear()
                for surgery_data in surgeries_data:
                    surgery, _ = Surgery.objects.get_or_create(**surgery_data)
                    medical_history.surgeries.add(surgery)

                medical_history.save()
