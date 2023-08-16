from django.utils import timezone
from libary_shop.models import Book,Loan,CustomUser
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, time, timedelta
from django.core.exceptions import ValidationError  
from .forms import UpdateBookForm
from django.contrib.auth.decorators import user_passes_test



# Create your views here.

def not_logged_in(request):
    return render(request, 'not_logged_in.html')


def is_superuser(user):
    return user.is_superuser

def books(request):
    search_text = request.GET.get('search_text')
    all_books = Book.objects.all()

    if search_text:
        all_books = all_books.filter(name__icontains=search_text)  # Change 'name' to the appropriate field name for book titles

    return render(request, 'index.html', {'all_books': all_books})


@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def books_on_rent(request):
    user = request.user
    # print("Logged in user:", user)
    
    active_loans = Loan.objects.filter(customer=user, loan_date__lte=timezone.now(), return_date__gte=timezone.now())
    # print("Active Loans:", active_loans)  

    # for loan in active_loans:
    #     print(f"Loan: customer={loan.customer}, book={loan.book}, loan_date={loan.loan_date}, return_date={loan.return_date}")
    
    return render(request, 'books_on_rent.html', {'active_loans': active_loans})


@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def books_available(request):
    # Fetch all loans that are currently active (loan_date is not in the future and return_date is null or in the future)
    active_loans = Loan.objects.filter(loan_date__lte=timezone.now(), return_date__gte=timezone.now())

    # Get the list of Book objects from the active loans
    active_books = [loan.book for loan in active_loans]

    # Fetch all books that are not in the active_books list
    active_books = Book.objects.exclude(pk__in=[book.pk for book in active_books])

    # Pass the books_not_on_rent to the template
    return render(request, 'active_books.html', {'active_books': active_books})


def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print(f"** login passed. user is:{user}")
            return redirect('all_books')  # Redirect to the homepage after successful login
        else:
            print(f"!! error login. user is:{user}")
            # If authentication fails, show an error message or redirect back to the login page
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('all_books')


def register(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')
        city = request.POST.get('city')
        age = request.POST.get('age')

        if new_username and new_password and city and age:
            try:
                # Check if the username is already taken
                existing_user = CustomUser.objects.get(username=new_username)
                # If user with the same username exists, raise an exception
                raise ValueError('The username is already taken.')
            except CustomUser.DoesNotExist:
                # If the user with the same username does not exist, create a new user
                user = CustomUser.objects.create_user(username=new_username, password=new_password)
                # Set additional fields for the user (city and age)
                user.city = city
                user.age = age
                user.save()  # Save the user profile with the city and age

                # Automatically log in the user after successful registration
                login(request, user)
                return redirect('all_books')  # Redirect to a page after successful registration
            except Exception as e:
                # Handle other exceptions, if any
                return redirect('registration_failed')  # Redirect to a generic registration failed page

    return render(request, 'register.html', {'user': request.user})


def registration_failed(request):
    return render(request, 'registration_failed.html')


@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def loan_book(request):
    if request.method == 'GET' and 'book_id' in request.GET:
        book_id = request.GET['book_id']
        book = get_object_or_404(Book, pk=book_id)
        print("****loan book****")

        # Check if the book is already on loan
        if Loan.objects.filter(book=book, return_date__isnull=True).exists():
            return redirect('Books_available')  # Book already on loan
        
        # Calculate return_date based on the book type's maximum loan days
        max_loan_days = Loan.get_max_loan_days(None, book.book_type)  # Pass the book_type
        loan_date = timezone.now()  # Use the current time for loan_date
        return_date = loan_date + timedelta(days=max_loan_days)
        
        # Create a new loan instance with calculated return_date
        loan = Loan.objects.create(customer=request.user, book=book, loan_date=loan_date, return_date=return_date)
        loan.save

        return redirect('Books_available')  # Book successfully loaned
    
    return redirect('Books_available')  # Invalid or missing book_id


@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def return_book(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')

        try:
            loan = Loan.objects.get(id=loan_id)
            print("Loan found:", loan)
            
            # Delete the loan
            loan.delete()
            
        except Loan.DoesNotExist:
            print("Loan does not exist.")

    return redirect('Books_rent')  # Redirect to appropriate view after returning


def custom_404(request, exception):
    return render(request, '404.html', status=404)

@user_passes_test(is_superuser)
@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def display_all_loans(request):
    all_loans = Loan.objects.all()
    return render(request, 'all_loans.html', {'all_loans': all_loans})

@user_passes_test(is_superuser)
@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in    
def add_book(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_author = request.POST.get('author')
        new_year_published = request.POST.get('year_published')
        new_book_type = request.POST.get('book_type')
        new_image = request.FILES.get('image')  # Use request.FILES for file uploads

        # print(new_name,new_author,new_year_published,new_book_type,new_image)


        if new_name and new_author and new_year_published and new_book_type and new_image:
            new_book = Book(name=new_name, author=new_author, year_published=new_year_published, book_type=new_book_type, image=new_image)
            try:
                new_book.full_clean()  # Validate the fields
                new_book.save()  # Save the new book instance to the database
                # print(new_book)

                return redirect('all_books')  # Redirect to a page after successful book addition
            except ValidationError as e:
                # Handle validation errors, if any
                pass  # You can customize error handling here

    return render(request, 'add_book.html', {'Book': Book})  # Pass the Book model to the template context


@user_passes_test(is_superuser)
@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def remove_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('all_books')  # Redirect to a page after successful remove book


@user_passes_test(is_superuser)
@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = UpdateBookForm(request.POST, request.FILES, instance=book)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('all_books')  # Redirect after successful update
    else:
        form = UpdateBookForm(instance=book)

    return render(request, 'update_book.html', {'form': form})
