import requests
from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Rating
from .serializers import RatingSerializer

PRODUCT_SERVICE_URL = "http://localhost:8004/api/products/"

class RatingListCreateView(APIView):
    def get(self, request, product_id=None):
        if product_id:
            ratings = Rating.objects.filter(product_id=product_id)
        else:
            ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            product_id = serializer.data['product_id']

            # Fetch all ratings for the product
            ratings = Rating.objects.filter(product_id=product_id)
            avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']

            if avg_rating is not None:
                # Update product's avg_rating
                update_response = requests.put(f"{PRODUCT_SERVICE_URL}{product_id}/", json={"avg_rating": float(round(avg_rating, 1))})

                if update_response.status_code != 200:
                    return Response({"error": "Failed to update avg_rating"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingDetailView(APIView):
    def get_object(self, customer_id, product_id):
        try:
            return Rating.objects.get(customer_id=customer_id, product_id=product_id)
        except Rating.DoesNotExist:
            return None

    def get(self, request, customer_id, product_id):
        rating = self.get_object(customer_id, product_id)
        if rating:
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        return Response({"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, customer_id, product_id):
        rating = self.get_object(customer_id, product_id)
        if rating:
            rating.delete()
            return Response({"message": "Rating deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)
