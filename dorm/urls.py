from . import views
from django.urls import path


app_name = "dorm"
urlpatterns = [
    path('callback/', views.callback, name="callback"),
    path('dorm_users/', views.dorm_users, name="payment"),
    path('pay_bill/', views.pay_bill, name="pay_bill"),
]
