from django import forms
from . models import *

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['bookid', 'name', 'author', 'price', 'description', 'photo', 'categories']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']