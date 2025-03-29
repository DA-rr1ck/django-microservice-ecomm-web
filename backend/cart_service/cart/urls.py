from django.urls import path
from .views import add_to_cart, get_cart, update_cart, remove_from_cart, checkout

urlpatterns = [
    path('cart/<int:customer_id>/', get_cart, name='get_cart'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/<int:customer_id>/', checkout, name='checkout'),
]
