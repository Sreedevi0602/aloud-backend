from django.shortcuts import render,redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from . models import *
from rest_framework.response import Response
from . serializer import *
from . forms import *
from django.http import JsonResponse
from django.http import HttpResponse

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
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_categories')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get(self, request, id):
        category = Category.objects.get(id=id)  # Fetch category by id
        serializer = CategorySerializer(category)  # Serialize the data
        return Response(serializer.data)  # Return the serialized data as JSON

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'category_detail.html', {'category': category})