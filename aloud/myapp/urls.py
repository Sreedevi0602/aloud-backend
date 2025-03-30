from django.urls import path
from . import views
from myapp.views import *

urlpatterns = [
    path('addbook/',views.addbook,name="addbookurl"),
]