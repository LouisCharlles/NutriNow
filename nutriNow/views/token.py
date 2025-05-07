from rest_framework_simplejwt.views import TokenObtainPairView
from ..serial import CustomTokenObtainPairAndIdSerializer

class CustomTokenObtainPairAndIdView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairAndIdSerializer