from django.urls import path

from home.director.views import Dashboard, Clients, Customers, getchangechartdash, getchangechartdashbug, Clientsun, mijoz_detail, \
    blocked

urlpatterns = [
    path('', Dashboard.as_view(), name='director-dashboard'),
    path('client', Clients.as_view(), name="client"),
    path('clientun', Clientsun.as_view(), name="clientun"),
    path('customers', Customers.as_view(), name="customers"),
    
    path('getchangechartdash', getchangechartdash, name="getchangechartdash"),
    path('getchangechartdashbug', getchangechartdashbug, name="getchangechartdashbug"),
    #mijoz detail
    path('mijoz/<int:id>', mijoz_detail, name='mijoz'),
    path('blocked/<int:id>', blocked, name='bloklash'),
    
]