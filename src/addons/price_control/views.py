from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PageSerializer
from .models import Page


class PriceControllPageViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Page.objects.filter(product__alarm_user=self.request.user)
