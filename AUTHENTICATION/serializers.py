from rest_framework import serializers

from .models import User

from BOOK.service import BookService

from BOOK.serializers import BookSerializer



class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
class UserSerializer(serializers.ModelSerializer):
    rented_books = serializers.SerializerMethodField()
    
    def get_rented_books(self, obj):
        return BookSerializer(BookService.list_user_rented_books(user=obj), many=True).data
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'rented_books']
        
        