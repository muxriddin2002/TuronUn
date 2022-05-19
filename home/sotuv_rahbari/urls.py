from django.urls import path
from home.sotuv_rahbari.view import *


urlpatterns = [
    path("", Dashboard.as_view(), name="sotuv_rahbar_dashboard"),
    #ajax
    path('ajax/load-ombor',ajax_load_ombor, name='ajax_load_ombor'),
    #active orders
    path("get-active-orders", GetActiveOrder.as_view(), name="sotuv-rahbari-get-active-orders"),
    # path('active-order-detail/<int:pk>', OrderDetailActive.as_view(), name='sotuvchi-order-detail-active'),
    #seller
    path('seller-list', SellerList.as_view(), name='sotuv-rahbari-seller-list'),
    path('seller-list2', SellerListJadval.as_view(), name='sotuv-rahbari-seller-list2'),
    path('seller-detail/<int:pk>', SellerDetail.as_view(), name='sotuv-rahbari-seller-detail'),
    #ombor
    path('ombor/<int:id>',ombor_detail, name='ombor_detail'),
    #Mijozlar list
    path('mijozlar', Customers.as_view(), name="mijozlar"),
    #set plan to seller
    path('set-plan/', set_plan, name="set_plan"),
    #filter
    path('getdashdetalsotuv', getdashdetalsotuv, name="getdashdetalsotuv"),
    # ajax mijozlar filter
    path('get-dash-detail-mijoz',getdashdetailmijoz, name='getdashdetailmijoz'),
    # ajax hudud filter
    path('get-dash-detail-hudud-summa', getdashhududsumma, name='getdashhududsumma'),
    # ajax seller hudud sum filter
    path('get-dash-detail-seller-hudud-summa',getdashsellerhududsumma, name='getdashsellerhududsumma'),

    ]