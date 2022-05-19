from django.urls import path

from home.Tarozi_hisobchi.view import *
urlpatterns = [
    path('', Dashboard.as_view(), name='tarozi-dashboard'),
    
    path('akt-list', AktView.as_view(), name='akt-list'),
    path('create-akt-post', create_akt_post, name='create-akt-post'),
    path('akt-detail', akt_detail, name="akt-detail"),
    path('akt-detail-post', akt_detail_post, name="akt-detail-post"),
    
    #un akt
    path('un-list', UnView.as_view(), name='un-list'),
    path('create-akt-un', create_akt_un, name='create-akt-un'),             #n
    #CRUD
    path('aktun-detail', aktun_detail, name="aktun-detail"),                #n
    path('aktun-detail-post', aktun_detail_post, name="aktun-detail-post"),       #n
    path('aktun-detail-edit', aktun_detail_edit, name="aktun-detail-edit"),         #n
    path('aktun-detail-delete', aktun_detail_delete, name="aktun-detail-delete"),       #n
    
    path('clientsun', ClientunView.as_view(), name='clientsun'),
    
    path('akt-detail-edit', akt_detail_edit, name="akt-detail-edit"),
    path('akt-detail-delete', akt_detail_delete, name="akt-detail-delete"),
    path('akt-hisobot', AktHisobot.as_view(), name='akt-hisobot'),
    path('akt-hisobot-detail/<int:pk>', AktHisobotDetail.as_view(), name='akt-hisobot-detail'),
    path('clients', ClientView.as_view(), name='clients'),
    
    path('un-ombori', UnOmborView.as_view(), name='un-ombori'),
    path('yem-ombori', YemOmborView.as_view(), name='yem-ombori'),
    
    path('ajax/load-tegirmon-products', ajax_load_tegirmon_products_un, name='ajax_load_tegirmon_products'),
    path('ajax/load-tegirmon-yem', ajax_load_tegirmon_yem, name='ajax_load_tegirmon_yem'),
    
    path('get-dashdetail', Getdashdetail, name="get-dashdetail"),
    path('getchangechartdashun', getchangechartdashun, name="getchangechartdashun"),
    path('craete-client', craeteclient, name="craete-client"),
    path('craete-clientun', craeteclientun, name="craete-clientun"),
    path('getchangechartdashtar', getchangechartdashtar, name="getchangechartdashtar"),

]
