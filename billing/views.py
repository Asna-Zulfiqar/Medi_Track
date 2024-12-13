from datetime import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from billing.models import HospitalBill, Accountant
from billing.serializers import HospitalBillSerializer
from billing.tasks import send_bill_email_to_patient
from billing.utils import generate_bill
from staff.permissions import IsPatientGroup , IsAccountantGroup

class BillRequestView(APIView):
    """
     Just a simple view to request for the bill
    """
    permission_classes = [IsAuthenticated , IsPatientGroup]

    def post(self, request, *args, **kwargs):

        patient = request.user.patient_profile
        data = request.data
        pdf_content = generate_bill(patient.id)
        send_bill_email_to_patient.delay(patient_id=patient.id, pdf_content=pdf_content)


        return Response(
            {
                "message": "Your bill request has been processed.",
            },
            status=status.HTTP_200_OK,
        )

class HospitalBillListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAccountantGroup]
    serializer_class = HospitalBillSerializer

    def get_queryset(self):
        """
        Fetch hospital bills associated with the authenticated accountant.
        """
        try:
            accountant = Accountant.objects.get(user=self.request.user)
        except Accountant.DoesNotExist:
            # Handle the case where the user is not an Accountant
            return HospitalBill.objects.none()  # Return an empty queryset

        return HospitalBill.objects.filter(accountant=accountant)


class HospitalBillBatchUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAccountantGroup]

    def get(self, request):
        """
        Fetch all hospital bills.
        """
        bills = HospitalBill.objects.all()
        serialized_bills = HospitalBillSerializer(bills, many=True)
        return Response(serialized_bills.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Handle batch updates for hospital bills, allowing multiple bills to be updated at once.
        """
        bill_ids = request.data.get('bill_ids', [])
        status_value = request.data.get('status', None)  # Renamed status to avoid conflict
        amount_paid = request.data.get('amount_paid', None)

        if not bill_ids:
            return Response({"error": "No hospital bill IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        if status_value not in ['paid', 'unpaid']:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the bills
        bills = HospitalBill.objects.filter(id__in=bill_ids)
        if not bills.exists():
            return Response({"error": "No hospital bills found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Get the current accountant
        accountant = request.user.accountant_profile  # Assuming the user is linked to an accountant instance

        # Update each bill
        updated_bills = []
        for bill in bills:
            bill.status = status_value
            bill.amount_paid = amount_paid if amount_paid else bill.amount_paid
            bill.accountant = accountant  # Assign the current accountant
            if status_value == 'paid' and bill.status != 'paid':
                bill.paid_on = timezone.now()
            bill.save()
            updated_bills.append(HospitalBillSerializer(bill).data)

        # Fetch all the hospital bills after the update
        all_bills = HospitalBill.objects.all()
        all_bills_data = HospitalBillSerializer(all_bills, many=True).data

        return Response({
            "message": "Hospital bills updated successfully.",
            "updated_bills": updated_bills,
            "all_bills": all_bills_data
        }, status=status.HTTP_200_OK)
