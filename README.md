# Library Project (Django)

This project is a management system for a library, built using a combination of HTML, Django, PostgreSQL, JavaScript, and CSS.

## Features

### Superuser Features
- Add books to the library
- Remove books from the library
- Update book details
- Cancel loans
- View all loans and identify overdue loans

### Regular User Features
- Loan books
- Return books
- View the remaining loan time
- See available books for loan
- See their own loans

## Accessing the Site

You can access the live site here: [Library Project](https://django-libary.onrender.com/libary_shop/)

### Superuser Access
To access the site as a superuser:
- Username: ofer
- Password: 1234

### Regular User Access
To access the site as a regular user:
- Register on the site or log in using your credentials

## Running Locally

To run the project locally:
1. Create a new folder and open it in your preferred code editor.
2. Clone the repository: `git clone https://django-libary.onrender.com/libary_shop/`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `.\venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install project dependencies: `pip install -r requirements.txt`
6. Create a superuser account: `python manage.py createsuperuser`
7. Start the development server: `python manage.py runserver`

## Usage

1. Access the local development server at `http://127.0.0.1:8000/`.
2. Explore the different features based on whether you're logged in as a superuser or a regular user.

## Site Navigation

The project site has two access modes: superuser and regular user. Each mode has its own set of features tailored to the user type.


## Authors

- Ofer Karp

