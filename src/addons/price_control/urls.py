from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'pages', views.PriceControllPageViewSet, basename='Page')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('product/<int:id>/stats/', views.AuditViewSet.as_view())
]