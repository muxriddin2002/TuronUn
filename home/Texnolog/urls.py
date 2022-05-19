from django.urls import path

from home.Texnolog.views import *

urlpatterns = [
    path('', Dashboard.as_view(), name="texnolog-dashboard"),
    path('akt-set-quality', AktSetQualityView.as_view(), name="texnolog-akt-set-quality"),
    path('akt-set-comment', akt_set_comment, name="texnolog-akt-set-comment"),
    path('wheats', WheatHistoryView.as_view(), name="texnolog-wheats"),
    path('add-wheats', add_wheat, name="texnolog-add-wheats"),
    path('edit-wheats', edit_wheat, name="texnolog-edit-wheats"),
    path('status-wheats', change_status_wheat, name="texnolog-status-wheats"),
    path('create_barcodes', CreateBarcodes.as_view(), name="create_barcodes"),
    path('add_barcode', add_barcode, name="add_barcode"),
    path('barcode/<int:pk>', barcode, name="barcode"),
    path('getdashdetailtexnolog', getdashdetailtexnolog, name="getdashdetailtexnolog"),
    path('getchangecharttex', getchangecharttex, name="getchangecharttex"),
    path('statistics', statistics, name="statistics"),
    path('difference', difference, name="difference"),
    path('add-tarozi-soni', addtarozisoni, name="add-tarozi-soni"),
    path('brak', Brak.as_view(), name="brak"),
]