from django.urls import path
from home.yordamchi_bugalter.views import Clients


urlpatterns = [
    path('', Clients.as_view(), name="yordamchi_bugalter_dashboard"),
]