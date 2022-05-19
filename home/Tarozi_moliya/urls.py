from django.urls import path

from home.Tarozi_moliya.view import *

urlpatterns = [
    path('', Dashboard.as_view(), name="tarozi-moliya-dashboard"),
    path('aktlar', AktView.as_view(), name="tarozi-moliya-aktlar"),
    path('unaktlar', UnAktView.as_view(), name="tarozi-moliya-unaktlar"),
    path('akt-detail/<int:pk>', AktChiqimDetail.as_view(), name="tarozi-moliya-aktlar-chiqim"),
    path('unakt-detail/<int:pk>', UnAktChiqimDetail.as_view(), name="tarozi-moliya-unaktlar-chiqim"),

    path('add-type-outlay', add_type_outlay, name='tarozi-molia-add-type-outlay'),
    path('add-untype-outlay', add_untype_outlay, name='tarozi-molia-add-untype-outlay'),
    path('add-outlay', add_outlay, name='tarozi-molia-add-outlay'),
    path('add-unoutlay', add_unoutlay, name='tarozi-molia-add-unoutlay'),

    path('add-qop', add_qop, name='tarozi-molia-add-qop'),
    
    path('set-price', set_price, name='tarozi-molia-set-price'),
    path('set-unprice', set_unprice, name='tarozi-molia-set-unprice'),
    path('set-price-qop', set_price_qop, name='tarozi-molia-set-price-qop'),
    path('qop-ombor', QopView.as_view(), name='tarozi-molia-qop-ombor'),
    path('qop-ombor-active', QopViewActive.as_view(), name='tarozi-molia-qop-ombor-active'),
    path('getdashdetailmoliya', Getdashdetailmoliya, name='getdashdetailmoliya'),
    path('changekgofclient', changekgofclient, name='changekgofclient'),

]