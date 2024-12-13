from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from feedback.models import Feedback, DoctorFeedback, ServiceFeedback, StaffFeedback
from staff.models import Receptionist, SecurityGuard, Sweeper, Nurse


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['patient', 'reviews', 'rating', 'created_at']
        read_only_fields = ['patient' , 'created_at']

class DoctorFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorFeedback
        fields = ['patient', 'doctor', 'reviews', 'rating', 'created_at']
        read_only_fields = ['patient', 'created_at']

class ServiceFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeedback
        fields = ['patient', 'service', 'reviews', 'rating', 'created_at']
        read_only_fields = ['patient', 'created_at']

class StaffFeedbackSerializer(serializers.ModelSerializer):
    # ChoiceField to select the staff model
    staff_model = serializers.ChoiceField(
        choices=[
            (ct.id, ct.model) for ct in ContentType.objects.filter(
                model__in=['receptionist', 'securityguard', 'sweeper', 'nurse']
            )
        ],
        write_only=True,
    )
    staff_id = serializers.IntegerField(write_only=True)
    staff_users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StaffFeedback
        fields = [ 'reviews', 'created_at', 'rating', 'staff_model', 'staff_id', 'staff_users']

    def get_staff_users(self, obj):
        # Fetch users dynamically for allowed models
        allowed_models_mapping = {
            'receptionist': Receptionist.objects.all(),
            'securityguard': SecurityGuard.objects.all(),
            'sweeper': Sweeper.objects.all(),
            'nurse': Nurse.objects.all(),
        }

        user_data = {}
        for model_name, queryset in allowed_models_mapping.items():
            user_data[model_name] = [
                {"id": user.id, "name": str(user)} for user in queryset
            ]
        return user_data

    def create(self, validated_data):
        # Extract staff_model and staff_id
        staff_model_id = validated_data.pop('staff_model')
        staff_id = validated_data.pop('staff_id')

        # Retrieve the ContentType and assign it
        staff_content_type = ContentType.objects.get(id=staff_model_id)

        # Create the feedback object
        feedback = StaffFeedback.objects.create(
            staff_content_type=staff_content_type,
            staff_object_id=staff_id,
            **validated_data
        )
        return feedback