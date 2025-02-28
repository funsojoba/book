from .models import Book, RentedBook
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from .serializers import BookSerializer, RentBookSerializer, RentedBookSerializer



class BookService:
    @classmethod
    def list_book(cls, **kwargs):
        books = Book.objects.filter(**kwargs)
        return True, books, 200

    @classmethod
    def create_book(cls, **kwargs):
        try:
            book = Book.objects.create(**kwargs)
            return True, book, 201
        except Exception as e:
            return False, {"message": str(e)}, 400

    @classmethod
    def update_book(cls, book, **kwargs):
        for key, value in kwargs.items():
            setattr(book, key, value)
        book.save()
        return True, book, 200

    @classmethod
    def get_book(cls, **kwargs):
        book = Book.objects.filter(**kwargs).first()
        return True, book, 200

    @classmethod
    def delete_book(cls, book):
        book.delete()
        return True, {"message": "Book deleted successfully."}, 204
    
    @classmethod
    def rent_book(cls, book:Book, user, **kwargs):
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')

        
        if book.rented:
            return False, {"message": "The book is already rented."}, 400

        if from_date > to_date:
            return False, {"message": "from_date cannot be later than to_date."}, 400
        
        rent_book = RentedBook.objects.create(
            book=book,
            user=user,
            from_date=from_date,
            to_date=to_date
        )
        book.rented = True
        book.rented_by = user
        book.save()
        return True, rent_book, 201
        
    
    @classmethod
    def return_book(cls, book):
        rented_book = RentedBook.objects.filter(book=book, is_returned=False).first()
        if not rented_book:
            return False, {"message": "The book is not rented."}, 400
        
        rented_book.is_returned = False
        rented_book.save()
        book.rented = False
        book.save()
        return True, rented_book, 200
    
    @classmethod
    def list_not_rented_books(cls, **kwargs):
        books = Book.objects.filter(rented=False, **kwargs)
        return Response(BookSerializer(books, many=True).data)
        

    @classmethod
    def list_rented_books(cls, **kwargs):
        books = Book.objects.filter(rented=True, **kwargs)
        return Response(BookSerializer(books, many=True).data)
    
    @classmethod
    def list_user_rented_books(cls, user):
        books = Book.objects.filter(rented=True, rented_by=user)
        return books
    