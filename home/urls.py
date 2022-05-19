from django.urls import path, include
from .views import login_view, logout_view, homeView, customeredit

urlpatterns = [
    path('',homeView, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tarozi-hisobchi/', include('home.Tarozi_hisobchi.urls')),
    path('tarozi-moliya/', include('home.Tarozi_moliya.urls')),
    path('sotuvchi/', include('home.sotuvchi.urls')),
    path('texnolog/', include('home.Texnolog.urls')),
    path('kassir/', include('home.Kassir.urls')),
    path('bugalter/', include('home.bugalter.urls')),
    path('director/', include('home.director.urls')),
    path('sotuv_rahbari/', include('home.sotuv_rahbari.urls')),
    path('operator/', include('home.operator.urls')),
    path('ombor-kassir/', include('home.ombor_kassir.urls')),
    path('yordamchi-bugalter/', include('home.yordamchi_bugalter.urls')),
    path('customer-edit/', customeredit, name='customeredit'),
    path('hujjatchi/', include('home.hujjatchi.urls')),

]

