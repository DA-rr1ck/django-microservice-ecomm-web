from django.urls import path
from .views import CreateShipmentView, ShipmentDetailView, UpdateShipmentStatusView

urlpatterns = [
    path('shipments/', CreateShipmentView.as_view(), name='create-shipment'),
    path('shipments/<int:order_id>/', ShipmentDetailView.as_view(), name='shipment-details'),
    path('shipments/update_status/<int:order_id>/', UpdateShipmentStatusView.as_view(), name='update-shipment-status'),
]
