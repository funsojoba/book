from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from helpers.custom_permission import IsAdminUser

from drf_yasg.utils import swagger_auto_schema

from .service import BookService
from .serializers import BookSerializer, RentBookSerializer, RentedBookSerializer
from .models import Book

from rest_framework.decorators import permission_classes




class BookViewSet(ViewSet):
    @permission_classes([AllowAny])
    def list(self, request):
        flag, books, _ = BookService.list_book()
        title = request.query_params.get('title')
        author = request.query_params.get('author')
        rented = request.query_params.get('rented')
        
        if author is not None:
            books = books.filter(author__icontains=author)
        if rented is not None:
            rented = rented.lower() == 'true'
            books = books.filter(rented=rented)
        if title is not None:
            books = books.filter(title__icontains=title)
        
        return Response(BookSerializer(books, many=True).data)
    
    def retrieve(self, request, pk=None):
        flag, book, status_ = BookService.get_book(id=pk)
        if book:
            return Response(BookSerializer(book).data)
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    @action(methods=['POST'], detail=True, url_path='rent', url_name='rent')
    def rent_a_book(self, request, pk=None):
        serializer = RentBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        flag, book, status_ = BookService.get_book(id=pk)
        if book:
            rent_flag, rent_book, rent_status = BookService.rent_book(book=book, user=request.user, **serializer.validated_data)
            if rent_flag:
                return Response(RentedBookSerializer(rent_book).data)
            return Response(rent_book, status=rent_status)
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['POST'], detail=True, url_path='return', url_name='return')
    def return_a_book(self, request, pk=None):
        book = BookService.get_book(id=pk)
        if book:
            flag, return_book, status_ = BookService.return_book(book=book)
            if flag:
                return Response({"message": "Book returned successfully."})
            return Response(return_book, status=status_)

        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    

class AdminBookView(ViewSet):
    permission_classes = [IsAdminUser]
    
    def list(self, request):
        books = BookService.list_book()
        return Response(BookSerializer(books, many=True).data)
    
    @swagger_auto_schema(request_body=BookSerializer)
    def create(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        book = BookService.create_book(**serializer.validated_data)
        
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        book = BookService.get_book(id=pk)
        if book:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            book = BookService.update_book(book, **serializer.validated_data)
            
            return Response(BookSerializer(book).data)
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        book = BookService.get_book(id=pk)
        if book:
            book.delete()
            return Response({"message": "Book deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def retrieve(self, request, pk=None):
        book = BookService.get_book(id=pk)
        if book:
            return Response(BookSerializer(book).data)
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    
    