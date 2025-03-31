from django.http import JsonResponse
from rest_framework.decorators import api_view
import tensorflow as tf
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler

# Load trained TensorFlow model once
model = tf.keras.models.load_model("recommendation/recommendation_model.h5")

# Use the correct loss function
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Product Service API URL
PRODUCT_SERVICE_API = "http://localhost:8004/api/products/"

def fetch_product_data():
    """Fetch product statistics from product_service API."""
    response = requests.get(PRODUCT_SERVICE_API)
    
    if response.status_code != 200:
        return []

    return response.json()  # Assuming it returns a list of products

@api_view(["GET"])
def get_recommendations(request):
    """API to get recommended products based on the trained model."""
    products = fetch_product_data()
    if not products:
        return JsonResponse({"error": "Failed to fetch product data"}, status=500)

    # Extract features
    product_ids = []
    data = []
    
    for product in products:
        product_ids.append(product["id"])
        data.append([
            product.get("view_count", 0),
            product.get("cart_count", 0),
            product.get("order_count", 0),
            product.get("avg_rating", 0.0)
        ])

    # Convert to numpy array
    X = np.array(data)

    # Normalize data (important for correct predictions)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Predict recommendation scores
    scores = model.predict(X_scaled).flatten()

    # Combine product IDs with scores
    recommendations = [{"product_id": product_id, "score": float(score)} for product_id, score in zip(product_ids, scores)]

    # Sort by score and return top 10
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return JsonResponse({"recommended_products": recommendations[:10]})
