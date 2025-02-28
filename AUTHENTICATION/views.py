from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from .serializers import SignUpSerializer, LoginSerializer, UserSerializer
from .service import AuthService, UserService

from rest_framework.response import Response
from rest_framework import status


class AuthViewSet(ViewSet):

    @swagger_auto_schema(request_body=SignUpSerializer)
    @action(methods=["POST"], detail=False)
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = AuthService._create_user(**serializer.validated_data)
        
        return user
    
    @swagger_auto_schema(request_body=LoginSerializer)
    @action(methods=["POST"], detail=False)
    def log_in(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = AuthService.login_user(**serializer.validated_data)
        
        return user
    
    
class UserViewSet(ViewSet):
    @action(methods=["GET"], detail=False)
    def me(self, request):
        return Response(UserSerializer(request.user).data)
    
    def list(self, request):
        users = UserService.list_users()
        
        return Response(UserSerializer(users, many=True).data)
    
    def retrieve(self, request, pk=None):
        user = UserService.get_user(id=pk)
        if user:
            return Response(UserSerializer(user).data)
        return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)