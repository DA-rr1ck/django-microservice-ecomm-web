import tensorflow as tf
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler

# URL of Product Service API
PRODUCT_SERVICE_API = "http://localhost:8004/api/products/"

def fetch_data():
    """Fetch product statistics from product_service API."""
    response = requests.get(PRODUCT_SERVICE_API)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch product data")

    products = response.json()  # Assuming product_service returns a list of products
    data = []
    product_ids = []

    for product in products:
        product_ids.append(product["id"])
        data.append([
            product.get("view_count", 0),
            product.get("cart_count", 0),
            product.get("order_count", 0),
            product.get("avg_rating", 0.0)
        ])

    return np.array(data), product_ids

# Load and Normalize Data
X, product_ids = fetch_data()
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)  # Normalize between 0 and 1

# Define Neural Network Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1, activation="linear")  # Output a continuous score
])

model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])

# Generate Labels: A better way would be using real-world user interaction data
y = X_scaled.mean(axis=1)  # Simple heuristic: weighted mean of interactions

# Train Model
model.fit(X_scaled, y, epochs=20, batch_size=8)
model.save("recommendation_model.h5")  # Save the model
