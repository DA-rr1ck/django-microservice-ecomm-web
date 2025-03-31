from django.urls import path
from .views import RatingListCreateView, RatingDetailView

urlpatterns = [
    path('ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('ratings/<str:product_id>/', RatingListCreateView.as_view(), name='rating-list-by-product'),
    path('ratings/<int:customer_id>/<str:product_id>/', RatingDetailView.as_view(), name='rating-detail'),
]
