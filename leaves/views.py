from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from leaves.models import Leave
from leaves.serializers import LeaveSerializer
from staff.permissions import IsStaffMember
from staff.permissions import IsAdministrator
from leaves.tasks import send_leave_applied_email_to_administrator , send_leave_email_to_staff


class LeaveApplicationView(CreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated , IsStaffMember]

    def perform_create(self, serializer):
        leave_instance = serializer.save(user=self.request.user)

        send_leave_applied_email_to_administrator.delay(
            user_name=leave_instance.user.get_full_name(),
            leave_reason=leave_instance.reason,
            start_date=leave_instance.start_date,
            end_date=leave_instance.end_date
        )

        # Send a confirmation email to the staff (user) who applied for leave
        send_leave_email_to_staff.delay(
            user_email=leave_instance.user.email,
            user_name=leave_instance.user.get_full_name(),
            start_date=leave_instance.start_date,
            end_date=leave_instance.end_date,
            status='Applied'
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Leave application submitted successfully."},
            status=status.HTTP_201_CREATED
        )

class LeaveDetailView(APIView):
    permission_classes = [IsAuthenticated , IsAdministrator]

    def get(self, request):

        leaves = Leave.objects.all()
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):

        leave_id = request.data.get('id')
        if not leave_id:
            return Response({"error": "Leave ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            leave = Leave.objects.get(id=leave_id)
        except Leave.DoesNotExist:
            return Response({"error": "Leave not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and validate data
        serializer = LeaveSerializer(leave, data=request.data, partial=True)
        if serializer.is_valid():
            updated_leave = serializer.save()

            # Send email to staff member about updated leave
            send_leave_email_to_staff.delay(
                user_email=updated_leave.user.email,
                user_name=updated_leave.user.get_full_name(),
                start_date=updated_leave.start_date,
                end_date=updated_leave.end_date,
                status=updated_leave.status
            )

            return Response(
                {"message": "Leave updated successfully.", "leave": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
