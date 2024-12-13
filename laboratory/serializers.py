from rest_framework import serializers
from laboratory.models import LabTestAllocation, Laboratory, Test
from django.utils import timezone
from medical_records.models import LabPrescription
from medical_records.models import TestResult
from laboratory.validators import validate_pdf

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['lab_prescription', 'patient', 'result', 'file']

    def validate_file(self, value):
        # Validate if the file is a PDF
        validate_pdf(value)
        return value


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class LaboratorySerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = Laboratory
        fields = ['id' , 'lab_name', 'email', 'opening_hours', 'closing_hours', 'contact', 'tests']


class LabTestAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestAllocation
        fields = ['id', 'prescription', 'laboratory', 'allocated_on', 'status', 'patient']
        read_only_fields = ['id', 'patient', 'allocated_on']

    def validate_laboratory(self, value):
        """Validate whether the laboratory can conduct the test and is open."""

        # Get the prescription object from the request data
        prescription_id = self.initial_data.get('prescription')
        if not prescription_id:
            raise serializers.ValidationError("Prescription is required.")

        try:
            # Fetch the related LabPrescription object using the ID
            lab_prescription = LabPrescription.objects.get(id=prescription_id)
        except LabPrescription.DoesNotExist:
            raise serializers.ValidationError("The specified prescription does not exist.")

        # Access the test_name from the LabPrescription
        test_name = lab_prescription.test.test_name

        # Check if the laboratory is open
        current_time = timezone.now().time()
        if not value.is_open():
            raise serializers.ValidationError(f"{value.lab_name} is closed at the moment.")

        # Check if the laboratory can conduct the requested test
        if not value.tests.filter(test_name=test_name).exists():
            raise serializers.ValidationError(f"{value.lab_name} cannot conduct the requested test: {test_name}.")

        return value
