from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Book(models.Model):
    class BookType(models.TextChoices):
        TYPE_10_DAY = '1', 'Up to days 10 loan'
        TYPE_5_DAY = '2', 'Up to 5 days loan'
        TYPE_2_DAY = '3', 'Up to 2 days loan'

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year_published = models.IntegerField()
    book_type = models.CharField(max_length=1, choices=BookType.choices)
    image = models.ImageField(upload_to="books_images", default="/books_images/books.png")


    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
    
class Loan(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField()

    def __str__(self):
        return f"{self.customer.username} - {self.book.name}"
    
    def get_max_loan_days(self, book_type):
        if book_type == Book.BookType.TYPE_10_DAY:
            return 10
        elif book_type == Book.BookType.TYPE_5_DAY:
            return 5
        elif book_type == Book.BookType.TYPE_2_DAY:
            return 2
        else:
            return 0

