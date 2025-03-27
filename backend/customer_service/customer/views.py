from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Customer
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["message"] = "User registered successfully."
        return response

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            "message": "Login successful.",
            "user": serializer.validated_data
        })

class ProfileView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = Customer.objects.get(id=user_id)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
