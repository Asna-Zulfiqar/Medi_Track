from rest_framework import serializers
from doctors.models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields = ['username', 'age' ,'blood', 'specialization', 'ward','contact',
                  'experience' , 'shift_timings' , 'is_available' ]

    def get_username(self, obj):
        return obj.user.username

