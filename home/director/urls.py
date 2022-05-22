from django.urls import path
from home.operator.views import OrderList, OrderDetails
from home.bugalter.views import Qop_clients
from home.sotuv_rahbari.view import SellerList, SellerDetail
from home.Texnolog.views import Brak
from home.bugalter.views import Kassa, BankKassa, Sms
from home.Tarozi_hisobchi.view import UnOmborView, YemOmborView
from home.Tarozi_moliya.view import QopView
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
    #operator active orders
    path('active-orders', OrderList.as_view(), name='director-active-orders'),
    path('active-orders-details/<int:pk>', OrderDetails.as_view(), name='director-active-orders-detail'),

    #bugalter qop clients
    path('qop-clients/', Qop_clients.as_view(), name="director-qop_clients"),

    #seller list
    path('seller-list', SellerList.as_view(), name='director-seller-list'),
    path('seller-detail/<int:pk>', SellerDetail.as_view(), name='director-seller-detail'),

    #brak
    path('brak', Brak.as_view(), name="director-brak"),

    #kassa
    path('kassa/', Kassa.as_view(), name='director-kassa'),
    path('bank-kassa/', BankKassa.as_view(), name='director-bank-kassa'),
    path('sms', Sms.as_view(), name="director-sms"),

    # tarozi hisobchi
    path('un-ombori', UnOmborView.as_view(), name='director-un-ombori'),
    path('yem-ombori', YemOmborView.as_view(), name='director-yem-ombori'),

    #tarozi moliya
    path('qop-ombor', QopView.as_view(), name='director-tarozi-molia-qop-ombor'),
]