from django.urls import path
from . import views
from myapp.views import *

urlpatterns = [
    path('addbook/', addbook, name='addbookurl'),  
    path('booklist/', booklist, name='booklisturl'),  
    path('api/books/', book_list, name='book-list-url'),
    path('api/books/<str:bookid>/', views.book_detail, name='book-detail-url')
]