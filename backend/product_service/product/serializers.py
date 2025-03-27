from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB uses ObjectId
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    price = serializers.FloatField()
    stock = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
