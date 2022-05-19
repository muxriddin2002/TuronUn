from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from home.api.urls import router
from django.conf.urls import url
# from rest_framework.schemas import get_schema_view #schemas va dokumentla
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Turon API',
        description="Turon Un Company",
        default_version='v1',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email="algoritmgateway@gmail.com"),
        license=openapi.License(name='TuronUn License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

def handler404(request,exception):
    return render(request, '404.html', status=404)
def handler500(request):
    return render(request, '500.html', status=500)
def check500(request):
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.api.urls')),
    path('api/store/', include(router.urls)),
    path('', include('home.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('check/', check500),
    #documents
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
#handlers
handler404 = handler404
handler500 = handler500