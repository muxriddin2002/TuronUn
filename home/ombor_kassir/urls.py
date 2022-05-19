from django.urls import path
from home.ombor_kassir.view import Dashboard


urlpatterns = [
    path('', Dashboard.as_view(), name="ombor_kassa_dashboard"),
]