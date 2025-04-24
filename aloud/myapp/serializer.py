from rest_framework import serializers
from . models import *

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['bookid', 'name', 'author', 'price', 'description', 'photo']

class CategorySerializer(serializers.ModelSerializer):
    books = BooksSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'books']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None
