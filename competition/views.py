from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import  login, logout
#from .models import
from django.urls import reverse
# Create your views here.
# testing git

def hello(request):
    return HttpResponse("hello")
