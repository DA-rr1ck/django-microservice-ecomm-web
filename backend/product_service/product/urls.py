from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="product-list"),
    path("products/<str:product_id>/", ProductDetailView.as_view(), name="product-details"),
]
