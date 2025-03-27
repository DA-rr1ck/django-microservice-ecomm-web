import requests
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer

PAYMENT_SERVICE_URL = "http://localhost:8004/api/payments/"

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        order_data = request.data
        items = order_data.get("items", [])
        total_price = sum(item["quantity"] * item["price"] for item in items)

        order = Order.objects.create(
            customer_id=order_data["customer_id"],
            total_price=total_price,
            payment_method=order_data["payment_method"],
            status="pending"
        )

        # Create order items in bulk
        order_items = [
            OrderItem(order=order, product_id=item["product_id"], quantity=item["quantity"], price=item["price"])
            for item in items
        ]
        OrderItem.objects.bulk_create(order_items)

        self.trigger_payment(order.id, order.customer_id, total_price, order.payment_method)

        # **Trigger Payment or Shipping**
        # if order.payment_method == "COD":
        #     self.trigger_shipping(order.id, order.customer_id)
        # else:
        #     self.trigger_payment(order.id, total_price, order.customer_id)

        return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

    def trigger_payment(self, order_id, customer_id, amount, payment_method):
        """Notify `payment_service` for payment processing."""
        data = {
            "order_id": order_id,
            "customer_id": customer_id,
            "amount": amount,
            "payment_method": payment_method
        }
        try:
            response = requests.post(PAYMENT_SERVICE_URL, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Payment Service Error: {e}")

    # def trigger_shipping(self, order_id, customer_id):
    #     """Notify `shipping_service` for COD orders."""
    #     data = {"order_id": order_id, "customer_id": customer_id}
    #     try:
    #         response = requests.post(SHIPPING_SERVICE_URL, json=data)
    #         response.raise_for_status()
    #     except requests.RequestException as e:
    #         print(f"Shipping Service Error: {e}")

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"

class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["paid", "en-route", "completed", "cancelled"]:
            return Response({"error": "Invalid status update"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({"message": f"Order status updated to {new_status}"}, status=status.HTTP_200_OK)
