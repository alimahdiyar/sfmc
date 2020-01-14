from . import views
from django.urls import path


app_name = "invoice"
urlpatterns = [
    path("<int:pk>/pay/", views.pay_invoice_view, name="hello"),
]