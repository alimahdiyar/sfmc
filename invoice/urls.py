from . import views
from django.urls import path


app_name = "invoice"
urlpatterns = [
    path('callback/', views.callback, name="callback"),
    # path('pay/', views.pay_view, name="payment"),
]
