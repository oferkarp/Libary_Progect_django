from django.urls import path

from libary_shop import views

urlpatterns = [
    path('', views.books, name='all_books'),
    path('Books_available_for_rent/', views.books_available, name='Books_available'),
    path('Books_on_rent/', views.books_on_rent, name='Books_rent'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'), 
    path('register/', views.register, name='register'),
    path('registration_failed/', views.registration_failed, name='registration_failed'),
    path('not_logged_in/', views.not_logged_in, name='not_logged_in'),


]