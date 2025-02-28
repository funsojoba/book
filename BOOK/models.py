from django.db import models

from helpers.db_helper import BaseAbstractModel
from django.contrib.auth import get_user_model


User = get_user_model()



class Book(BaseAbstractModel):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rented = models.BooleanField(default=False)
    rent_start_date = models.DateTimeField(null=True, blank=True)
    rent_end_date = models.DateTimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    rented_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = "books"

    def __str__(self):
        return self.title
    

class RentedBook(BaseAbstractModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rented_books")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    is_returned = models.BooleanField(default=False)
    
    class Meta:
        db_table = "rented_books"
    
    def __str__(self):
        return f"{self.book.title} - {self.user.display_name}"