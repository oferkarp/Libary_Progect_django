from django.shortcuts import render

from libary_shop.models import Book,Loan,CustomUser

# Create your views here.

def books(request):
    all_books = Book.objects.all()
    return render(request, 'index.html', {'all_books': all_books})
