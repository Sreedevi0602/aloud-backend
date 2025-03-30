from django.shortcuts import render,redirect
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
from . forms import *
from django.http import JsonResponse
from django.http import HttpResponse

# Create your views here.
