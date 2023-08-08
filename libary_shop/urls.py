from django.urls import path

from libary_shop import views

urlpatterns = [
    path('', views.books, name='all_books'),
    path('/Books_available_for_rent', views.Books_available_for_rent, name='Books_available'),
    path('/Books_not_on_rent', views.Books_not_on_rent, name='Books_rent'),

]