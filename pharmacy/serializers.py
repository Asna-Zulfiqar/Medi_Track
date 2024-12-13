from rest_framework import serializers
from pharmacy.models import Pharmacy, Medicine, MedicineAllocation


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'medicine_name', 'stock', 'expiration_date', 'price', 'reorder_level']

class PharmacySerializer(serializers.ModelSerializer):
    medicines = MedicineSerializer(many=True, read_only=True)  # Display medicines as read-only

    class Meta:
        model = Pharmacy
        fields = ['id', 'pharmacy_name', 'email', 'opening_hours', 'closing_hours', 'contact', 'medicines']


class MedicineAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineAllocation
        fields = ['patient', 'pharmacy', 'medicine', 'quantity', 'allocated_at']
        read_only_fields = ['allocated_at' , 'patient']

    def validate(self, data):
        medicine = data.get('medicine')
        quantity = data.get('quantity')

        if medicine.stock < quantity:
            raise serializers.ValidationError("Not enough stock available in the pharmacy.")

        if medicine.is_expired():
            raise serializers.ValidationError("The requested medicine is expired.")

        return data

    def create(self, validated_data):
        # Deduct the medicine quantity from the stock
        medicine = validated_data['medicine']
        quantity = validated_data['quantity']
        medicine.stock -= quantity
        medicine.save()
        return MedicineAllocation.objects.create(**validated_data)