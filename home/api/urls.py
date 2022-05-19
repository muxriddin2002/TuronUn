from django.urls import path
from .api_view import *
from .api_ombor import *
from .api_mobil import *
from .sotuv import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('storehistory', StoreHistoryViewset)
router.register('order', OrderViewset)
router.register('productionhistory', ProductionHistoryViewset)
router.register('returned_products', Return_productViewset)
router.register('qaytuv', QaytuvViewset)
router.register('securitysended', TurnofCarsViewset)
router.register('securitysendedtashkent', TurnofCarsofTashkentViewset)


urlpatterns = [
    #login
    path('login/', login),
    # Bugdoy
    path('get_clients/', get_client),
    # tegirmonlar
    path('get_branch/', get_branch),
    path('get_akt/', get_akts),
    path('get_active_akt/', get_akts_aktive),
    path('add_wagon/', add_wagons),
    path('get_akt_wagon/', get_akt_wagon),
    path('get_akt_wagon_all/', get_akt_wagon_all),
    path('edit-wagon/', wagon_edit),
    #android api
    path('get_unakts_ombors/', get_unakts_ombors),
    path('set_unakt_status/', set_unakt_status),
    path('get_unakts/', get_unakts),
    path('get_unakt_wagon/', get_unakt_wagon),
    path('get_unakt_wagon_all/', get_unakt_wagon_all),
    path('unwagon_edit/', unwagon_edit),
    path('get_unakts_aktive/', get_unakts_aktive),
    path('get_unclient/', get_unclient),
    path('add_unwagons/', add_unwagons),
    # Store
    path('add_store/', add_store),
    path('get_store_history/', get_store_history),
    path('get_product/', get_product),
    path('accept_store/', accept_store),
    path('return_product/', return_product),
    path('changestatusofhistory/', changestatusofhistory),
    path('get_store_product/', get_store_product),
    path('edit_store_product/', edit_store_product),
    path('get_brigada/', get_brigada),
    path('send_order/', send_order),
    path('load_order_basket/', load_order_basket),
    path('load_qaytuv_basket/', load_qaytuv_basket),
    path('get_qaytuv_basket/', get_qaytuv_basket),
    path('get_qaytuv/', get_qaytuv),
    path('get_order/', get_order),
    path('get_basket/', get_basket),
    path('add_brigada_tobasket/', add_brigada_tobasket),
    path('get_basket_product/', get_basket_product),
    path('get_load_qaytuv_basket/', get_load_qaytuv_basket),
    # security
    path('get_order_to_give_turn/', get_order_to_give_turn),
    path('reject_order/', reject_order),
    path('reject_turned_order/', reject_turned_order),
    path('add_turn/', add_turn),
    path('add_turn_and_enter_car/', add_turn_and_enter_car),
    path('get_turns/', get_turns),
    path('get_turn/', get_turn),
    path('get_all_waiting/', get_all_waiting),
    path('get_all_turn/', get_all_turn),
    path('enter_car/', enter_car),
    path('car_leave/', car_leave),
    path('get_basket_forsecurity/', get_basketforsecurity),
    # path('load_basket/', load_basket),
    path('get_active_turn/', get_active_turn),
    path('get_loading_turn/', get_loading_turn),
    path('get_passive_turn/', get_passive_turn),
    #barcode
    path('add_barcode/', add_barcode),
    path('products/', products),
    #qop
    path('get_clients_qop/', get_clients_qop),
    path('get_tin_qoldiq/', get_tin_qoldiq),
    path('get_history_of_tin/', get_history_of_tin),
    #qob tamnotchisi
    path('create_client_tin/', add_client_tin),
    path('get_qop_ombor/', get_qop_ombor),
    path('create_tin/', create_tin),
    path('return_income_qop/', return_income_qop), #return kirim qob 
    path('get_returned_income_qop/', get_returned_income_qop), # get returned kirim qob 
    path('get_returned_expanse_qop/', get_returned_expanse_qop), # get returned chiqim qob 
    path('expance_qop/', expance_qop), # chiqim create
    path('qop_chiqim_tarixi/', qop_chiqim_tarixi),
    path('return_expanse_qop/', return_expanse_qop), #return chiqim qob 
    path('get_type_of_tin/', get_type_of_tin),
    path('filter_statistics/', filter_statistics),
    #brak maxsulotni qabul qiliw
    path('returnedproducts/', ReturnedProducts),
    path('confirmreturned/', ConfirmReturned),
    path('filter_returned/', filter_returned),
    path('returnedproductshistory/', ReturnedProductsHistory),
    #delete order
    path('delete_orderla/', delete_order),
    path('user-firebase-token/', user_firebase_token),
    
] 
#connect to viewset
urlpatterns += router.urls