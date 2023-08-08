from django.urls import path

from libary_shop import views

urlpatterns = [
    path('', views.books, name='all_books'),
]