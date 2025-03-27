from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

    def create(self, validated_data):
        # Ensure only one shipment per order
        if Shipment.objects.filter(order_id=validated_data['order_id']).exists():
            raise serializers.ValidationError({"error": "Shipment for this order already exists."})
        return super().create(validated_data)
