from rest_framework import serializers
from wards.models import Ward, Bed, WardManager

class WardSerializer(serializers.ModelSerializer):
    beds = serializers.StringRelatedField(many=True, read_only=True)
    managers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Ward
        fields = ['id', 'ward_type', 'capacity', 'beds', 'managers']


class BedSerializer(serializers.ModelSerializer):
    ward_name = serializers.ReadOnlyField(source='ward.get_ward_type_display')

    class Meta:
        model = Bed
        fields = ['id', 'ward', 'ward_name', 'status', 'created_at']


class WardManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = WardManager
        fields = ['id', 'ward', 'shift']
