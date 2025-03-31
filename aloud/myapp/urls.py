from django.urls import path
from . import views
from myapp.views import *

urlpatterns = [
    path('addbook/', addbook, name='addbookurl'),  
    path('booklist/', booklist, name='booklisturl'),  
]