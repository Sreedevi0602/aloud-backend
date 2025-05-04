from rest_framework import serializers
from . models import *
from django.contrib.auth import authenticate

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
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'userid']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
'''
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid Credentials")
'''

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            print("Email not found")
            raise serializers.ValidationError("Invalid Credentials")

        print(f"Found user: {user_obj.username}")

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            print("Authentication failed for valid email")
            raise serializers.ValidationError("Invalid Credentials")

        data['user'] = user
        return data