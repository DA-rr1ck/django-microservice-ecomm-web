import requests
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer

ORDER_SERVICE_URL = "http://localhost:8003/api/orders/"
SHIPPING_SERVICE_URL = "http://localhost:8006/api/shipments/"

class CreatePaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        payment = Payment.objects.get(id=response.data['id'])

        # Handle payment based on method
        if payment.payment_method == "cod":
            payment.status = "pending"
            payment.save()

            requests.post(SHIPPING_SERVICE_URL, json={
                "order_id": payment.order_id,
                "customer_id": payment.customer_id
            })
        elif payment.payment_method == "transfer":
            # Simulate bank transfer processing (in real case, use payment gateway API)
            payment.transaction_id = "TXN-" + str(payment.id)
            payment.status = "paid"
            payment.save()

            requests.post(SHIPPING_SERVICE_URL, json={
                "order_id": payment.order_id,
                "customer_id": payment.customer_id
            })

        return response

class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = "order_id" 

class UpdatePaymentStatusView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = "order_id"

    def update(self, request, *args, **kwargs):
        payment = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["pending", "paid", "failed"]:
            return Response({"error": "Invalid status update"}, status=status.HTTP_400_BAD_REQUEST)

        payment.status = new_status
        payment.save()
        return Response({"message": f"Payment status updated to {new_status}"}, status=status.HTTP_200_OK)