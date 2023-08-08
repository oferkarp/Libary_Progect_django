from django.shortcuts import render
from django.utils import timezone
from libary_shop.models import Book,Loan,CustomUser

# Create your views here.

def books(request):
    search_text = request.GET.get('search_text')
    all_books = Book.objects.all()

    if search_text:
        all_books = all_books.filter(name__icontains=search_text)  # Change 'name' to the appropriate field name for book titles

    return render(request, 'index.html', {'all_books': all_books})


def Books_not_on_rent(request):
    # Fetch all loans that are currently active (loan_date is not in the future and return_date is null or in the future)
    active_loans = Loan.objects.filter(loan_date__lte=timezone.now(), return_date__gte=timezone.now())

    # Get the list of Book objects from the active loans
    books_not_on_rent = [loan.book for loan in active_loans]

    # Pass the active_books to the template
    return render(request, 'books_not_on_rent.html', {'books_not_on_rent': books_not_on_rent})

def Books_available_for_rent(request):
    # Fetch all loans that are currently active (loan_date is not in the future and return_date is null or in the future)
    active_loans = Loan.objects.filter(loan_date__lte=timezone.now(), return_date__gte=timezone.now())

    # Get the list of Book objects from the active loans
    active_books = [loan.book for loan in active_loans]

    # Fetch all books that are not in the active_books list
    active_books = Book.objects.exclude(pk__in=[book.pk for book in active_books])

    # Pass the books_not_on_rent to the template
    return render(request, 'active_books.html', {'active_books': active_books})
