from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    return render(request, "index.html", {})

def regulations_view(request):
    return render(request, "regulations.html", {})

def clipart_view(request):
    return render(request, "clipart.html", {})

def project_view(request):
    return render(request, "project.html", {})

def idea_show_view(request):
    return render(request, "idea_show.html", {})

def virtual_lab_view(request):
    return render(request, "virtual_lab.html", {})

def history_view(request):
    return render(request, "history.html", {})
