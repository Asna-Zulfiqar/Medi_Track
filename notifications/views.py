from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import DeviceToken


class SaveDeviceTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required."}, status=400)

        DeviceToken.objects.update_or_create(user=request.user, defaults={"token": token})
        return Response({"message": "Device token saved successfully."})
