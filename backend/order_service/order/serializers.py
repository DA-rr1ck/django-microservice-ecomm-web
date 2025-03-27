from rest_framework import serializers
from .models import Order, OrderItem
import requests

PRODUCT_SERVICE_URL = "http://localhost:8003/api/products/"

def get_product_details(product_id):
    response = requests.get(f"{PRODUCT_SERVICE_URL}{product_id}/")
    if response.status_code == 200:
        return response.json() 
    return {"name": "Unknown Product", "price": 0}

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    def get_product_details(self, obj):
        return get_product_details(obj.product_id)

    class Meta:
        model = OrderItem
        fields = ["product_id", "quantity", "price", "product_details"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer_id", "total_price", "payment_method", "status", "items", "created_at"]
