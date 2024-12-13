from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from patients.models import Patient
from staff.models import Receptionist, Sweeper, Nurse, SecurityGuard
from staff.permissions import IsPatientGroup
from feedback.models import Feedback, ServiceFeedback, DoctorFeedback, StaffFeedback
from feedback.serializers import FeedbackSerializer, DoctorFeedbackSerializer, ServiceFeedbackSerializer, \
    StaffFeedbackSerializer

class FeedbackCreateView(CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def perform_create(self, serializer):
        # Get the patient linked to the logged-in user
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(patient=patient)


class DoctorFeedbackCreateView(CreateAPIView):
    queryset = DoctorFeedback.objects.all()
    serializer_class = DoctorFeedbackSerializer
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def perform_create(self, serializer):
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(patient=patient)


class ServiceFeedbackCreateView(CreateAPIView):
    queryset = ServiceFeedback.objects.all()
    serializer_class = ServiceFeedbackSerializer
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def perform_create(self, serializer):
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(patient=patient)

class CreateStaffFeedbackView(ListCreateAPIView):
    queryset = StaffFeedback.objects.all()
    serializer_class = StaffFeedbackSerializer
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def get_queryset(self):
        # Return all feedback for the logged-in user (patient)
        return StaffFeedback.objects.filter(patient=self.request.user)

    def list(self, request, *args, **kwargs):
        # List all staff members from allowed models
        allowed_models_mapping = {
            'receptionist': Receptionist.objects.all(),
            'securityguard': SecurityGuard.objects.all(),
            'sweeper': Sweeper.objects.all(),
            'nurse': Nurse.objects.all(),
        }

        staff_data = {}
        for model_name, queryset in allowed_models_mapping.items():
            staff_data[model_name] = [
                {"id": user.id, "name": str(user)} for user in queryset
            ]

        return Response({"staff_users": staff_data})

    def perform_create(self, serializer):
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(patient=patient)

class GetUserFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Check if the user is a doctor
        if hasattr(user, 'doctor_profile'):
            feedbacks = DoctorFeedback.objects.filter(doctor=user.doctor_profile)
            if feedbacks.exists():
                feedback_data = [
                    {
                        "review": feedback.review,
                        "rating": feedback.rating,
                        "created_at": feedback.created_at,
                    }
                    for feedback in feedbacks
                ]
                return Response({"feedback": feedback_data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No feedback for you."}, status=status.HTTP_404_NOT_FOUND)

        # Determine specific staff model and get ContentType
        staff_model = None
        if hasattr(user, 'receptionist_profile'):
            staff_model = user.receptionist_profile
        elif hasattr(user, 'securityguard_profile'):
            staff_model = user.securityguard_profile
        elif hasattr(user, 'sweeper_profile'):
            staff_model = user.sweeper_profile
        elif hasattr(user, 'nurse_profile'):
            staff_model = user.nurse_profile

        if staff_model:
            content_type = ContentType.objects.get_for_model(staff_model.__class__)
            feedbacks = StaffFeedback.objects.filter(staff_content_type=content_type, staff_object_id=staff_model.id)
            if feedbacks.exists():
                feedback_data = [
                    {
                        "review": feedback.reviews,
                        "rating": feedback.rating,
                        "created_at": feedback.created_at,
                    }
                    for feedback in feedbacks
                ]
                return Response({"feedback": feedback_data}, status=status.HTTP_200_OK)

        return Response({"message": "No feedback for you."}, status=status.HTTP_404_NOT_FOUND)