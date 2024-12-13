from datetime import timezone
from rest_framework import serializers
from billing.models import HospitalBill

class HospitalBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalBill
        fields = ['id', 'patient', 'bill_generated_on', 'status', 'paid_on', 'amount_paid', 'total_amount', 'accountant']
        read_only_fields = ['bill_generated_on', 'patient', 'total_amount']

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        amount_paid = validated_data.get('amount_paid', instance.amount_paid)
        accountant = validated_data.get('accountant', instance.accountant)

        if status == 'paid' and instance.status != 'paid':
            instance.paid_on = timezone.now()

        instance.status = status
        instance.amount_paid = amount_paid
        instance.accountant = accountant
        instance.save()

        return instance