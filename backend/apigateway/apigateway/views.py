from rest_framework.decorators import api_view
from .gateway import forward_request

# Endpoints for customer_service
@api_view(["POST"])
def register(request):
    """Handles register requests and forwards them to customer_service"""
    return forward_request("customer_service", "/api/register/", "POST", request)

@api_view(["POST"])
def login(request):
    """Handles login requests and forwards them to customer_service"""
    return forward_request("customer_service", "/api/login/", "POST", request)

@api_view(["GET"])
def get_customer_details(request, user_id):
    """Fetches customer details from customer_service"""
    return forward_request("customer_service", f"/api/profile/{user_id}/", "GET", request)

# Endpoints for cart_service
@api_view(["GET"])
def get_cart(request, user_id):
    """Fetches cart from cart_service"""
    return forward_request("cart_service", f"/api/cart/{user_id}/", "GET", request)

@api_view(["POST"])
def add_to_cart(request):
    """Add item to cart in cart_service"""
    return forward_request("cart_service", "/api/cart/add/", "POST", request)

@api_view(["PUT"])
def update_cart(request, cart_id):
    """Update cart details in cart_service"""
    return forward_request("cart_service", f"/api/cart/update/{cart_id}/", "PUT", request)

@api_view(["DELETE"])
def remove_from_cart(request, cart_id):
    """Remove item from cart in cart_service"""
    return forward_request("cart_service", f"/api/cart/remove/{cart_id}/", "DELETE", request)

@api_view(["POST"])
def checkout(request, user_id):
    """Checkout in cart_service"""
    return forward_request("cart_service", f"/api/cart/checkout/{user_id}/", "POST", request)

# Endpoints for order_service
@api_view(["POST"])
def create_order(request):
    """Handles order creation requests and forwards them to order_service"""
    return forward_request("order_service", "/api/orders/", "POST", request)

@api_view(["GET"])
def get_order_details(request, order_id):
    """Fetches order details from order_service"""
    return forward_request("order_service", f"/api/orders/{order_id}/", "GET", request)

@api_view(["PUT"])
def update_order_status(request, order_id):
    """Update order status to order_service"""
    return forward_request("order_service", f"/api/orders/update_status/{order_id}/", "PUT", request)

# Endpoints for product_service
@api_view(["GET"])
def get_product_list(request):
    """Fetches product list from product_service"""
    return forward_request("product_service", "/api/products/", "GET", request)

@api_view(["GET"])
def get_product_details(request, product_id):
    """Fetches product details from product_service"""
    return forward_request("product_service", f"/api/products/{product_id}/", "GET", request)

# Endpoints for payment_service
@api_view(["POST"])
def create_payment(request):
    """Handles payment creation requests (after placing an order) and forwards them to payment_service"""
    return forward_request("payment_service", "/api/payments/", "POST", request)

@api_view(["GET"])
def get_payment_details(request, order_id):
    """Fetches payment details from payment_service"""
    return forward_request("payment_service", f"/api/payments/{order_id}/", "GET", request)

@api_view(["PUT"])
def update_payment_status(request, order_id):
    """Update payment status to payment_service"""
    return forward_request("payment_service", f"/api/payments/update_status/{order_id}/", "PUT", request)

# Endpoints for shipment_service
@api_view(["POST"])
def create_shipment(request):
    """Handles shipment creation requests (after placing an order) and forwards them to shipment_service"""
    return forward_request("shipment_service", "/api/shipments/", "POST", request)

@api_view(["GET"])
def get_shipment_details(request, order_id):
    """Fetches shipments details from shipment_service"""
    return forward_request("shipment_service", f"/api/shipments/{order_id}/", "GET", request)

@api_view(["PUT"])
def update_shipment_status(request, order_id):
    """Update shipments status to shipment_service"""
    return forward_request("shipment_service", f"/api/shipments/update_status/{order_id}/", "PUT", request)

# Endpoints for review_service
@api_view(["POST"])
def create_review(request):
    """Handles review creation requests and forwards them to review_service"""
    return forward_request("review_service", "/api/ratings/", "POST", request)

@api_view(["GET"])
def get_reviews_by_product(request, product_id):
    """Fetches reviews by product from review_service"""
    return forward_request("review_service", f"/api/ratings/{product_id}/", "GET", request)

@api_view(["GET"])
def get_reviews_by_product_by_customer(request, user_id, product_id):
    """Fetches reviews by product made by a customer from review_service"""
    return forward_request("review_service", f"/api/ratings/{user_id}/{product_id}/", "GET", request)

# Endpoints for recommendation_service
@api_view(["GET"])
def get_recommendations(request):
    """Fetches recommended products from recommendation_service"""
    return forward_request("recommendation_service", "/api/recommendations/", "GET", request)
