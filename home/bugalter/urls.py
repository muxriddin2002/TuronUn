from django.urls import path

from home.bugalter.views import *

urlpatterns = [
    path('', Dashboard.as_view(), name="bugalter_dashboard"),
    #status 4 orders details
    path('bugalter-order-detail-passive/<int:id>', PassiveOrdersDetails, name="order-detail-passive"),
    path('bugalter_clients/', Clients.as_view(), name="bugalter_clients"),
    path('bugdoy_hisobi/', Bugdoy_hisob.as_view(), name="bugdoy_hisobi"),
    path('bugdoy_clients/', Bugdoy_clients.as_view(), name="bugdoy_clients"),
    path('bugalter_vozvrat/', Bugalter_vozvrat.as_view(), name="bugalter_vozvrat"),
    
    path('un_clients/', Un_clients.as_view(), name="un_clients"),
    path('changekurs', changekurs, name="changekurs"),
    path('client_informations/<int:pk>', client_informations, name='client_informations'),
    
    path('sumtodollor', sum_to_dollor, name="sum_to_dollor"),
    path('dollortosum', dollor_to_sum, name="dollor_to_sum"),
    path('kassa-converts', kassa_converts, name="kassa_converts"),
    #kirimi     
    path('paymentclient', paymentclient, name="paymentclient"),
    path('outincomepayment', outincomepayment, name="outincomepayment"),
    path('chiqimpayment', chiqimpayment, name="chiqimpayment"),
    path('paymentforwheat/', paymentforwheat, name="paymentforwheat"),
    path('paymentforun/', paymentforun, name="paymentforun"),
    path('paymentforqop/', paymentforqop, name="paymentforqop"),
    path('paymentakt/', paymentakt, name="paymentakt"),
    
    path('bugdoy_akt/<int:pk>', Bugdoy_akt, name='bugdoy_akt'),
    path('un_akt/<int:pk>', Un_akt, name='un_akt'),
    
    path('paymentoutlay', paymentoutlay, name='paymentoutlay'),
    path('paymentunoutlay', paymentunoutlay, name='paymentunoutlay'),
    path('givepaymentclient', givepaymentclient, name='givepaymentclient'),
    
    path('paymentclients/<int:pk>', paymentclients, name='paymentclients'),
    path('paymentwheathistory/<int:pk>', paymentwheathistory, name='paymentwheathistory'),
    path('paymentunhistory/<int:pk>', paymentunhistory, name='paymentunhistory'),
    path('paymentqophistory/<int:pk>', paymentqophistory, name='paymentqophistory'),
    
    path('get-dashdetailbug', getdashdetailbug, name='get-dashdetailbug'),
    path('get-changechart', getchangechart, name='get-changechart'),
    
    path('wheatexpances', wheatexpances, name='wheatexpances'),
    path('unexpances', unexpances, name='unexpances'),
    
    path('add-limit', addlimit, name='add-limit'),
    
    path('sms', Sms.as_view(), name="sms"),
    path('smsgateway', SmsGateway, name="smsgateway"),
    path('newsmstemplate', NewSMSTemplate_class.as_view(), name="newsmstemplate"),
    
    path('qop_clients/', Qop_clients.as_view(), name="qop_clients"),
    path('edit-bug-client/', editbugclient, name="edit-bug-client"),
    
    path('sms_template_status_change/', sms_template_status_change, name='sms_template_status_change'),
    path('search_lead/', search_lead, name='search_lead'),
    path('save_sms_template/', save_sms_template, name='save_sms_template'),
    #kassa
    path('kassa/', Kassa.as_view(), name='kassa'),
    path('bank-kassa/', BankKassa.as_view(), name='bank-kassa'),
    path('ajax-bank-shots/', ajax_bank_shots, name='ajax_bank_shots'),
    path('ajax-bank-chiqim-shots/', ajax_bank_chiqim_shots, name='ajax_bank_chiqim_shots'),
    path('ajax-bank-shots-data/', ajax_bank_shots_data, name='ajax_bank_shots_data'),
    path('ajax-bank-shots-chiqim-data/', ajax_bank_shots_chiqim_data, name='ajax_bank_shots_chiqim_data'),
    path('ajax_load_categories/', ajax_load_categories, name='ajax_load_categories'),
    path('edit-payhistory/', edit_payhistory, name='edit_payhistory'),
    

]