from rest_framework import serializers
from . models import *

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['bookid', 'name', 'author', 'price', 'category', 'description', 'photo']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']