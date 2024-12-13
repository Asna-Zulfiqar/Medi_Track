from rest_framework import serializers
from staff.models import Receptionist, SecurityGuard, Sweeper, Nurse
from billing.models import Accountant

class ReceptionistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptionist
        fields = ['age' , 'contact_number' , 'is_available' , 'shift']
        read_only_fields = ['user']


class SecurityGuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityGuard
        fields = ['age' , 'contact' , 'is_available' , 'shift_timings' , 'ward']
        read_only_fields = ['user']


class SweeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sweeper
        fields = ['age' , 'contact' , 'is_available' , 'shift_timings' , 'ward']
        read_only_fields = ['user']


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ['age' , 'contact' , 'is_available' , 'shift_timings' , 'ward']
        read_only_fields = ['user']

class AccountantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountant
        fields = ['age' , 'contact' , 'is_available' , 'shift_timings' , 'ward']
        read_only_fields = ['user']