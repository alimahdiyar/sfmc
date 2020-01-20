from . import views
from django.urls import path


app_name = "invoice"
urlpatterns = [
    path('callback/', views.callback, name="callback"),
    path('<int:team_pk>/pay', views.pay_team, name="payment"),
]
