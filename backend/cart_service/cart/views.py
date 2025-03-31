from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CartItem
from .serializers import CartItemSerializer
import requests

ORDER_SERVICE_URL = "http://localhost:8003/api/orders/"
PRODUCT_SERVICE_URL = "http://localhost:8004/api/products/"

# Get Cart Items
@api_view(['GET'])
def get_cart(request, customer_id):
    cart_items = CartItem.objects.filter(customer_id=customer_id)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)

# Add Item to Cart (Fetch Product from MongoDB)
@api_view(['POST'])
def add_to_cart(request):
    customer_id = request.data.get("customer_id")
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    # Fetch Product from MongoDB
    product_response = requests.get(f"{PRODUCT_SERVICE_URL}{product_id}/")
    if product_response.status_code != 200:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    product_data = product_response.json()
    product_name = product_data["name"]
    product_price = float(product_data["price"])

    product_cart_count = product_data["cart_count"] + 1

    # Save to Cart
    cart_item = CartItem.objects.create(
        customer_id=customer_id,
        product_id=product_id,
        name=product_name,
        quantity=quantity,
        price=product_price
    )

    requests.put(f"{PRODUCT_SERVICE_URL}{product_id}/", json={"cart_count": product_cart_count})
    
    return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

# Update Cart Item
@api_view(['PUT'])
def update_cart(request, cart_id):
    try:
        cart_item = CartItem.objects.get(id=cart_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Remove Item from Cart
@api_view(['DELETE'])
def remove_from_cart(request, cart_id):
    try:
        cart_item = CartItem.objects.get(id=cart_id)
        cart_item.delete()
        return Response({"message": "Cart item removed"}, status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

# Checkout (Send Cart to Order Service)
@api_view(['POST'])
def checkout(request, customer_id):
    cart_items = CartItem.objects.filter(customer_id=customer_id)
    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    # Prepare order data
    order_items = [{"product_id": item.product_id, "quantity": item.quantity, "price": str(item.price)} for item in cart_items]
    order_data = {
        "customer_id": customer_id,
        "items": order_items,
        "total_price": float(sum(item.quantity * item.price for item in cart_items)),
        "payment_method": request.data.get("payment_method", "cod"),
    }

    # Send order data to order_service
    response = requests.post(ORDER_SERVICE_URL, json=order_data)

    if response.status_code == 201:
        cart_items.delete()  # Clear cart after successful order
        return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to place order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
