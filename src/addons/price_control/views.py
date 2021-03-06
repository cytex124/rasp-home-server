from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PageSerializer, AuditLogSerializer, ProductSerializer
from .models import Page, AuditLog, Product
from rest_framework_tracking.mixins import LoggingMixin


class PriceControlPageViewSet(LoggingMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Page.objects.filter(product__alarm_user=self.request.user)


class AuditViewSet(LoggingMixin, APIView):
    serializer_class = AuditLogSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None, *args, **kwargs):
        """
        Returns a Response with AuditLogs and Product-Infos of a Product-Object.
        """
        product_id = kwargs.get('id', None)
        product = get_object_or_404(Product, id=product_id)
        audit_logs = AuditLog.objects.filter(page__product=product).order_by('page', '-created_at')[0:1000]
        audit_logs_data = AuditLogSerializer(audit_logs, many=True)
        return Response({
            'product': ProductSerializer(instance=product).data,
            'audit_logs': audit_logs_data.data
        }, status=status.HTTP_200_OK)
