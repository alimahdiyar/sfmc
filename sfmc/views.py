from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    return render(request, "index.html", {})

def regulations_view(request):
    return render(request, "regulations.html", {})
