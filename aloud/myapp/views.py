from django.shortcuts import render,redirect
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
        # Fetch the book by its bookid (which is a string)
        book = Books.objects.get(bookid=bookid)
    except Books.DoesNotExist:
        return Response(status=404)  # Return 404 if the book doesn't exist

    # Serialize the book details and return it in the response
    serializer = BooksSerializer(book)
    return Response(serializer.data)