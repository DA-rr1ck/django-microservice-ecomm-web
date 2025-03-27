from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        # Ensure an order is not processed twice
        if Payment.objects.filter(order_id=validated_data['order_id']).exists():
            raise serializers.ValidationError({"error": "Payment for this order already exists."})
        return super().create(validated_data)
