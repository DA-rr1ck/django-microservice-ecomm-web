from django.urls import path
from .views import register, login, get_customer_details, create_order, get_order_details, update_order_status, get_product_list, get_product_details, create_payment, get_payment_details, update_payment_status, create_shipment, get_shipment_details, update_shipment_status

urlpatterns = [
    # URLs for customer_service
    path("api/register/", register, name="register"),
    path("api/login/", login, name="login"),
    path("api/profile/<int:user_id>/", get_customer_details, name="get_customer_details"),

    # URLs for order_service

    # todo: add an endpoint to show all ongoing orders

    path("api/order/create/", create_order, name="create_order"),
    path("api/order/<int:order_id>/", get_order_details, name="get_order_details"),
    path("api/order/update_status/<int:order_id>/", update_order_status, name="update_order_status"),

    # URLs for product_service

    # todo: add an endpoint to add products

    path("api/products/", get_product_list, name="get_product_list"),
    path("api/product/<str:product_id>/", get_product_details, name="get_product_details"),

    # URLs for payment_service
    path('api/payment/create/', create_payment, name='create_payment'),
    path('api/payment/<int:order_id>/', get_payment_details, name='get_payment_details'),
    path('api/payment/update_status/<int:order_id>/', update_payment_status, name='update-payment-status'),

    # URLs for shipment_service
    path('api/shipment/create/', create_shipment, name='create_shipment'),
    path('api/shipment/<int:order_id>/', get_shipment_details, name='get_shipment_details'),
    path('api/shipment/update_status/<int:order_id>/', update_shipment_status, name='update_shipment_status'),

]
