from django.utils import timezone
from libary_shop.models import Book,Loan,CustomUser
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def books(request):
    search_text = request.GET.get('search_text')
    all_books = Book.objects.all()

    if search_text:
        all_books = all_books.filter(name__icontains=search_text)  # Change 'name' to the appropriate field name for book titles

    return render(request, 'index.html', {'all_books': all_books})

def not_logged_in(request):
    return render(request, 'not_logged_in.html')

@login_required(login_url='not_logged_in')  # Redirect to 'not_logged_in' view if user is not logged in
def books_on_rent(request):
    user = request.user
    print("Logged in user:", user)
    
    active_loans = Loan.objects.filter(customer=user, loan_date__lte=timezone.now(), return_date__gte=timezone.now())
    print("Active Loans:", active_loans)  # Add this line

    for loan in active_loans:
        print(f"Loan: customer={loan.customer}, book={loan.book}, loan_date={loan.loan_date}, return_date={loan.return_date}")
    
    return render(request, 'books_on_rent.html', {'active_loans': active_loans})


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
            return render(request, 'index.html', {'error_message': error_message})
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