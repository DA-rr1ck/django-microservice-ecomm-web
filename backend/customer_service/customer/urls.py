from django.urls import path
from .views import register_view, login_view, profile_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/<int:user_id>/', profile_view, name='customer-profile'),
]
