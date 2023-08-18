from django import forms
from .models import Book

class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'year_published', 'image']
