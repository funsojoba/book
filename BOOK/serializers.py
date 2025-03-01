from rest_framework import serializers
from .models import Book, RentedBook
from django.utils import timezone


class BookSerializer(serializers.ModelSerializer):
    
    available_on = serializers.SerializerMethodField()
    
    def get_available_on(self, obj):
        if obj.rented:
            latest_rented_book = obj.rented_books.order_by('-to_date').first()
            if latest_rented_book:
                return latest_rented_book.to_date
        return timezone.now().date()
    
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'description', 'price', 'rented', 'rented_by', 'available_on']
        
        
class RentBookSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    
    
class RentedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = RentedBook
        fields = "__all__"
