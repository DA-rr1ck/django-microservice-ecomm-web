from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bson import ObjectId  # Import to work with MongoDB IDs
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get_object(self, product_id):
        """Fetch product by MongoDB's ObjectId"""
        try:
            if not ObjectId.is_valid(product_id):  # Ensure ID format is valid
                return None
            return Product.objects.get(id=ObjectId(product_id))
        except Product.DoesNotExist:
            return None

    def track_view(self, product_id):
        """Increment the view count in Product"""
        product = self.get_object(product_id)
        product.view_count += 1
        product.save()

    def get(self, request, product_id):
        product = self.get_object(product_id)
        if product is None:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Track the view count
        self.track_view(product_id)

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, product_id):
        product = self.get_object(product_id)
        if product is None:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if product is None:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
