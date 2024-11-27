from rest_framework import serializers
from patients.models import Patient, Condition, Allergy, Surgery, MedicalHistory



class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'

class SurgerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Surgery
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    conditions = ConditionSerializer(many=True, required=False)
    allergies = AllergySerializer(many=True, required=False)
    surgeries = SurgerySerializer(many=True, required=False)

    class Meta:
        model = MedicalHistory
        fields = '__all__'
        read_only_fields = ['patient']

    def create(self, validated_data):
        conditions_data = validated_data.pop('conditions', [])
        allergies_data = validated_data.pop('allergies', [])
        surgeries_data = validated_data.pop('surgeries', [])
        medical_history = MedicalHistory.objects.create(**validated_data)

        for condition_data in conditions_data:
            condition, _ = Condition.objects.get_or_create(**condition_data)
            medical_history.conditions.add(condition)

        for allergy_data in allergies_data:
            allergy, _ = Allergy.objects.get_or_create(**allergy_data)
            medical_history.allergies.add(allergy)

        for surgery_data in surgeries_data:
            surgery, _ = Surgery.objects.get_or_create(**surgery_data)
            medical_history.surgeries.add(surgery)

        return medical_history

class PatientSerializer(serializers.ModelSerializer):
    medical_history = MedicalHistorySerializer(read_only=True, source='medical_histories', many=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'age', 'gender', 'contact',
            'emergency_contact', 'address', 'date_of_birth',
            'medical_history'
        ]
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include the username instead of user ID
        representation['user'] = instance.user.username
        return representation