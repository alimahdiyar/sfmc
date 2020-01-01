from . import views
from django.urls import path


app_name = "competition"
urlpatterns = [
    path("hello/", views.hello, name="hello"),
]
