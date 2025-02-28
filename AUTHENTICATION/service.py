import uuid

from rest_framework import status
from django.conf import settings
from django.contrib.auth.hashers import check_password

from .models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


from .serializers import UserSerializer


class AuthService:
    @classmethod
    def _create_user(cls, **kwargs) -> User:
        password = kwargs.get("password")
        email = kwargs.get("email")
        if User.objects.filter(email=email).exists():
            return Response(data={"error": "User with these credentials already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            phone_number=kwargs.get("phone_number"),
            email=kwargs.get("email")
        )
        user.set_password(password)
        user.save()
        
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

        

    @classmethod
    def set_user_password(cls, user, password):
        user.set_password(password)
        user.save()


    @classmethod
    def update_user(cls, user, **kwargs):
        avatar = kwargs.get("avatar")
        user.first_name = kwargs.get("first_name", user.first_name)
        user.last_name = kwargs.get("last_name", user.last_name)
        user.email = kwargs.get("email", user.email)
        user.phone_number = kwargs.get("phone_number", user.phone_number)
        user.save()
        return user


    @classmethod
    def get_user(cls, **kwargs):
        return User.objects.filter(**kwargs).first()



    @classmethod
    def login_user(cls, email, password):
        user = cls.get_user(email=email)

        if user:
            user_password = check_password(password, user.password)
            
            if not user_password:
                return Response(data={"error": "incorrect email/password"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken.for_user(user)
            data = {
                "user": UserSerializer(instance=user).data,
                "token": {"refresh": str(token), "access": str(token.access_token)},
            }
            return Response(data=data)
        return Response(data={"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def get_all_users(cls, **kwargs):
        return User.objects.filter(**kwargs)



class UserService:
    @classmethod
    def list_users(cls):
        return User.objects.all()
    
    @classmethod
    def list_user_books(cls, user):
        user_books = user.books.all()
        return user_books
    
    @classmethod
    def get_user(cls, **kwargs):
        user = User.objects.filter(**kwargs).first()
        return user
    
    @classmethod
    def delete_user(cls, user):
        user.delete()
        return True, {"message": "User deleted successfully."}, 204
    
    @classmethod
    def update_user(cls, user, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return True, user, 200