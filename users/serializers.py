from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [ 'username' , 'email' , 'first_name' , 'last_name' , 'groups' , 'is_active']

    def get_groups(self, obj):
        # Return the names of the groups the user belongs to
        return [group.name for group in obj.groups.all()]

class RegisterSerializer(serializers.ModelSerializer):
    role_choices = [
        ('Doctor' , 'Doctor'),
        ('Staff' , 'Staff'),
        ('Patient' , 'Patient'),
    ]

    role = serializers.ChoiceField(choices=role_choices)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password' , 'role']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
            }
        }

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)

        # Assign to group based on role
        group, created = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is not active.")

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Include user details
        data['user'] = {
            'username': user.username,
            'email': user.email,
            'role': user.groups.first().name if user.groups.exists() else None
        }
        return data
