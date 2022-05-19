from django.urls import path
from .views import Dashboard, OrderDetails


urlpatterns = [
    path('', Dashboard.as_view(), name="hujjatchi_dashboard"),
    path('order_detail/<int:pk>', OrderDetails.as_view(), name="hujjatchi-orders-detail")
    
]