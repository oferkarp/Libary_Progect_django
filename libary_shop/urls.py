from django.urls import path

from libary_shop import views

from django.conf.urls import handler404

handler404 = 'libary_shop.views.custom_404'


urlpatterns = [
    path('', views.books, name='all_books'),
    path('active_books/', views.books_available, name='Books_available'),
    path('Books_on_rent/', views.books_on_rent, name='Books_rent'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'), 
    path('register/', views.register, name='register'),
    path('registration_failed/', views.registration_failed, name='registration_failed'),
    path('not_logged_in/', views.not_logged_in, name='not_logged_in'),
    path('loan_book/', views.loan_book, name='loan_book'),
    path('return_book/', views.return_book, name='return_book'),
    path('all_loans/', views.display_all_loans, name='all_loans'),
    path('add_book/', views.add_book, name='add_book'),
    path('remove_book/<int:book_id>/', views.remove_book, name='remove_book'),
    path('update_book/<int:book_id>/', views.update_book, name='update_book'),

]
