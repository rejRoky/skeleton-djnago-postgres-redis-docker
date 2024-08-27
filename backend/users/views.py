from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnProfileOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]

    def get_object(self):
        """
        Override get_object to return the current user if the action is `retrieve`, `update`, or `partial_update`.
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return self.request.user
        return super().get_object()

    def perform_update(self, serializer):
        serializer.save()

@api_view(['POST'])
def login(request):
    mobile_number = request.data.get('mobile_number')
    password = request.data.get('password')
    user = authenticate(mobile_number=mobile_number, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
