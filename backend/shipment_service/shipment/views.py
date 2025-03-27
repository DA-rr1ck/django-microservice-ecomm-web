import requests
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Shipment
from .serializers import ShipmentSerializer

CUSTOMER_SERVICE_URL = "http://localhost:8001/api/profile/"
ORDER_SERVICE_URL = "http://localhost:8002/api/orders/"

class CreateShipmentView(generics.CreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def create(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        customer_id = request.data.get("customer_id")

        # Fetch Customer Address from customer_service
        customer_response = requests.get(f"{CUSTOMER_SERVICE_URL}{customer_id}/")
        if customer_response.status_code != 200:
            return Response({"error": "Failed to retrieve customer details"}, status=status.HTTP_400_BAD_REQUEST)

        customer_data = customer_response.json()
        customer_address = customer_data.get("address")

        # Save Shipment Record with Address
        shipment = Shipment.objects.create(
            order_id=order_id,
            customer_id=customer_id,
            address=customer_address,
            status="pending"
        )

        return Response(ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED)

class ShipmentDetailView(generics.RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    lookup_field = "order_id" 

class UpdateShipmentStatusView(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    lookup_field = "order_id"

    def update(self, request, *args, **kwargs):
        shipment = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["shipped", "delivered"]:
            return Response({"error": "Invalid status update"}, status=status.HTTP_400_BAD_REQUEST)

        # Update Shipment Status
        shipment.status = new_status
        shipment.save()

        # If delivered, update Order Status in order_service
        if new_status == "delivered":
            order_response = requests.put(
                f"{ORDER_SERVICE_URL}update_status/{shipment.order_id}/",
                json={"status": "completed"}
            )
            if order_response.status_code != 200:
                return Response({"error": "Failed to update order status"}, status=status.HTTP_400_BAD_REQUEST)
        elif new_status == "shipped":
            order_response = requests.put(
                f"{ORDER_SERVICE_URL}update_status/{shipment.order_id}/",
                json={"status": "en-route"}
            )
            if order_response.status_code != 200:
                return Response({"error": "Failed to update order status"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"Shipment status updated to {new_status}"}, status=status.HTTP_200_OK)
