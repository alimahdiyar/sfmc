from . import views
from django.urls import path


app_name = "invoice"
urlpatterns = [
    path('callback/', views.callback, name="callback"),
    path('<int:pk>/pay', views.pay_invoice_view, name="payment"),
]
