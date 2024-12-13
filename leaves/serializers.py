from rest_framework import serializers
from leaves.models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['id', 'user', 'start_date', 'end_date', 'reason', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user',  'created_at', 'updated_at']
