from django.urls import path, register_converter

from home.sotuvchi.view import *
from home.converts import FloatUrlParameterConverter

register_converter(FloatUrlParameterConverter, 'float')

urlpatterns = [
    #smart test
    path('ajax/load-products', load_products, name='ajax_load_products'),
    path('ajax/load-modal', load_modal, name='ajax_load_modal'),
    
    path("", Dashboard.as_view(), name="sotuvchi_dashboard"),
    path("get-order", GetOrder.as_view(), name="sotuvchi-get-order"),
    path("get-order-active", GetOrderActive.as_view(), name="sotuvchi-get-order-active"),
    path('get-order-passive', GetOrderPassive.as_view(), name='sotuvchi-get-order-passive'),
    path('mijozlar', Mijozlar.as_view(), name='mijozlar'),
    path("add-bonus", addbonus, name="add-bonus"),

    path('create-order', create_order, name='sotuvchi-create-order'),
    path('create-qaytuv', create_qaytuv, name='sotuvchi-create-qaytuv'),
    path('order-detail/<int:pk>', OrderDetail.as_view(), name='sotuvchi-order-detail'),
    path('order-detail-active/<int:pk>', OrderDetailActive.as_view(), name='sotuvchi-order-detail-active'),
    
    # add to basket via a href
    path('add-basket/<int:order_id>/<int:pro_id>/<str:narxi>/<str:qop_soni>', add_basket, name='sotuvchi-add-basket'),
    path('edit-basket/<int:order_id>/<int:pro_id_edit>/<str:narxi_edit>/<str:qop_soni_edit>/<int:e_id>/', edit_basket, name='sotuvchi-edit-basket'),
    path('delete-basket/<int:order_id>/<int:bk_id>', delete_basket, name='sotuvchi-delete-basket'),
    # CRUD via post
    path('add-basket', add_basket, name='sotuvchi-add-basket'),
    path('edit-basket', edit_basket, name='sotuvchi-edit-basket'),
    path('delete-basket', delete_basket, name='sotuvchi-delete-basket'),

    path('add-basket-qaytuv', add_basket_qaytuv, name='sotuvchi-add-basket-qaytuv'),
    path('delete-basket-qaytuv', delete_basket_qaytuv, name='sotuvchi-delete-basket-qaytuv'),
    path('edit-basket-qaytuv', edit_basket_qaytuv, name='sotuvchi-edit-basket-qaytuv'),
    path('get-qaytuv', GetQaytuv.as_view(), name="sotuvchi-get-qaytuv"),
    path('qaytuv-detail/<int:pk>', QaytuvDetail.as_view(), name="sotuvchi-qaytuv-detail"),
    path('get-dashdetailsel', getdashdetailsel, name="get-dashdetailsel"),
    path('getchangechartsel', getchangechartsel, name="getchangechartsel"),
    path('craete-customer', craetecustomer, name="craete-customer"),
    
    path('residual-branches', ResidualBranchesDetail.as_view(), name="residual-branches"),
    path('change-residue/<int:pk>', changeresidue, name="change-residue"),
    path('change-all-residue', changeallresidue, name="change-all-residue"),
    
    path('delete-order/<int:pk>', DeleteOrder, name="delete-order"),
    path('client_orders/<int:pk>', ClientOrder, name="client_orders"),
]
