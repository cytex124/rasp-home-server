"""hs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.static import serve


admin.site.site_header = 'Home-Server Backend'
admin.site.site_title = 'Home-Server Backend'
admin.site.site_url = ''
admin.site.index_title = 'Home-Server Backend'

schema_view = get_schema_view(
   openapi.Info(
      title="Home-Server API",
      default_version='v1',
      description="",
      terms_of_service="",
      contact=openapi.Contact(email="andreas.wyrobek95@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(IsAuthenticated,),
)


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


urlpatterns = [
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    re_path(r'^{0}(?P<path>.*)$'.format(settings.MEDIA_URL[1:]), protected_serve, {'document_root': settings.MEDIA_ROOT}),
]
