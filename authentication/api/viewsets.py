from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import * 

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

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
    else:
        return response.Response(serializer.data,status=status.HTTP_200_OK)

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def logout(request):
    serializer = UserLogoutSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return response.Response(status=status.HTTP_204_NO_CONTENT)

