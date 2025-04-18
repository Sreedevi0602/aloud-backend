from rest_framework import serializers
from . models import *

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['bookid', 'name', 'author', 'price', 'description', 'photo', 'categories']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']