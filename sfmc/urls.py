"""sfmc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('clipart/', views.clipart_view, name='clipart'),
    path('history/', views.history_view, name='history'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('hovercraft/', views.hovercraft_view, name='hovercraft'),
    path('virtual-lab/', views.virtual_lab_view, name='virtual_lab'),
    path('idea-show/', views.idea_show_view, name='idea_show'),
    path('project/', views.project_view, name='project'),
    path('regulations/', views.regulations_view, name='regulations'),
    path('', views.index_view, name='index'),
]
