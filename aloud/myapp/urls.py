from django.urls import path
from . import views
from myapp.views import *

urlpatterns = [
    path('addbook/', addbook, name='addbookurl'),  # Form page
    path('booklist/', booklist, name='booklisturl'),  # Table page
]