from django.shortcuts import render,redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from . models import *
from rest_framework.response import Response
from . serializer import *
from . forms import *
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.

def addbook(request):
    if request.method == "POST":
        form = BooksForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('booklisturl')  
    else:
        form = BooksForm()
    
    return render(request, 'addbook.html', {'form': form})

def booklist(request):
    books = Books.objects.all()
    return render(request, 'booklist.html', {'books': books})

def delete(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    book.delete()
    return redirect('booklisturl')

def edit(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    return render(request, "edit.html", {"book": book})

def update(request):
    if request.method == "POST":
        book_id = request.POST.get("id")
        book = get_object_or_404(Books, id=book_id)

        book.name = request.POST.get("name")
        book.author = request.POST.get("author")
        book.price = request.POST.get("price")
        book.category = request.POST.get("category")
        book.description = request.POST.get("description")

        if 'photo' in request.FILES:
            book.photo = request.FILES['photo']

        book.save()
        return redirect('booklisturl')  
    
@api_view(['GET'])
def book_list(request):
    books = Books.objects.all()
    serializer = BooksSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def book_detail(request, bookid):
    try:
        
        book = Books.objects.get(bookid=bookid)
    except Books.DoesNotExist:
        return Response(status=404)  

    
    serializer = BooksSerializer(book)
    return Response(serializer.data)

def create_categories(request):
    categories = Category.objects.all()
    return render(request, 'create_categories.html', {'categories': categories})



def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_categories')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get(self, request, id):
        category = Category.objects.get(id=id)  # Fetch category by id
        serializer = CategorySerializer(category)  # Serialize the data
        return Response(serializer.data)  # Return the serialized data as JSON

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books_in_category = Books.objects.filter(categories=category)
    return render(request, 'category_detail.html', {'category':category, 'books_in_category': books_in_category})

def assign_books_to_categories(request, category_id):
    all_books = Books.objects.all()
    all_categories = Category.objects.all()
    
    if request.method == 'POST':
        for book in all_books:
            key = f'book_{book.id}_categories'
            selected_cats = request.POST.getlist(key)
            if selected_cats:
                book.categories.set(selected_cats)  # Overwrites with new list
            else:
                book.categories.clear()  # Remove all categories if none selected
        return redirect('category_detail', category_id=category_id)

    return render(request, 'assign_books.html', {
        'all_books': all_books,
        'all_categories': all_categories,
        'category_id': category_id
    })

# API View - Register User
class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered'}, status=201)
        return Response(serializer.errors, status=400)

# API View - Login User
@method_decorator(csrf_protect, name='dispatch')
class LoginUser(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            request.session['username'] = user.username  # Save to session

            response_data = {
                'redirect_url': 'http://localhost:8000/userlist/' if user.is_superuser else 'http://localhost:5174/',
                'username': user.username
            }
            return Response(response_data)
        return Response(serializer.errors, status=400)
'''
class LoginUser(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            if user.is_superuser:
                return Response({'redirect_url': 'http://localhost:8000/userlist/'})
            return Response({'redirect_url': 'http://localhost:5174/'})
        return Response(serializer.errors, status=400)
'''

# API View - User List (JSON API for React if needed)
class UserList(APIView):
    def get(self, request):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# HTML View - User List (for Django Admin in users.html)
# @method_decorator(login_required, name='dispatch')
class UserListHTMLView(APIView):
    def get(self, request):
        users = CustomUser.objects.filter(is_superuser=False)
        return render(request, 'users.html', {'users': users})




#To get current user in the format "Hi Username" 
@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        return Response({'username': request.user.username})
    return Response({'username': None})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'userid': user.userid
    })

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})