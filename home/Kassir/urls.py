from django.urls import path

from home.Kassir.views import Dashboard, getdashdetailkassa, expance, addexpanse, addtypeexpanse

urlpatterns = [
    path('', Dashboard.as_view(), name="kassir-dashboard"),
    
    path('getdashdetailkassa', getdashdetailkassa, name="getdashdetailkassa"),
    #chiqim
    path('expance', expance, name="expance"),
    path('add-expanse', addexpanse, name="add-expanse"),
    path('add-type-expanse', addtypeexpanse, name="add-type-expanse"),
]