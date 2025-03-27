from django.urls import path
from .views import CreatePaymentView, PaymentDetailView, UpdatePaymentStatusView

urlpatterns = [
    path('payments/', CreatePaymentView.as_view(), name='create-payment'),
    path('payments/<int:order_id>/', PaymentDetailView.as_view(), name='payment-details'),
    path('payments/update_status/<int:order_id>/', UpdatePaymentStatusView.as_view(), name='update-payment-status'),
]
