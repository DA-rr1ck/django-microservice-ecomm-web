from django.urls import path
from .views import CreateOrderView, OrderDetailView, UpdateOrderStatusView

urlpatterns = [
    path('orders/', CreateOrderView.as_view(), name='create-order'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name="order-details"),
    path('orders/update_status/<int:id>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]
