from rest_framework import  status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.contrib.auth.models import User
from users.serializers import RegisterSerializer, LoginSerializer , UserSerializer
from django.contrib.auth import authenticate
from users.tasks import send_login_email , send_welcome_email

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send welcome email
        send_welcome_email.delay(user.email, user.username)

        return Response({
            "message": "User registered successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.groups.first().name if user.groups.exists() else None
            }
        },
            status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data

        # Sending token to email
        send_login_email.delay(
            subject="Your Login Token From Medi_Track",
            message=f"Access Token: {token_data['access']}",
            from_email="codingfalsafa@example.com",
            recipient_list=[user.email],
        )

        # Send push notification using Firebase
        # try:
        #     # Replace this with the stored Firebase device token of the user
        #     firebase_device_token = user.profile.device_token
        #     send_push_notification(
        #         token=firebase_device_token,
        #         title="Login Alert",
        #         body="You have successfully logged in to Medi_Track.",
        #     )
        # except Exception as e:
        #     return Response(
        #         {"message": "Login successful. Notification failed to send.", "error": str(e)},
        #         status=status.HTTP_200_OK
        #     )

        return Response({
            "message": "Login successful. Please check your email for the authentication token."
        },
            status=status.HTTP_200_OK
        )

class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user