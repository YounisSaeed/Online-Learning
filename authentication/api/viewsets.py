from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer

User = get_user_model()

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    result = {
        "refresh":str(refresh),
        "access":str(refresh.access_token)
    }
    return response.Response(result,status=status.HTTP_201_CREATED)