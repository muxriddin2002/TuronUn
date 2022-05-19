from django.urls import path
from home.operator.views import Dashboard, OrderList,OrderDetails, edit_operator_basket

urlpatterns = [
    path('', Dashboard.as_view(), name="operator-dashboard"),
    path('active_orders/', OrderList.as_view(), name="operator-aktiv-orders"),
    path('active_orders_detail/<int:pk>', OrderDetails.as_view(), name="operator-active-orders-detail"),
    path('edit_operator_basket/', edit_operator_basket, name="edit_operator_basket"),
]