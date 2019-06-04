from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, Page, AuditLog


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        exclude = ('alarm_user', )


class PageSerializer(ModelSerializer):
    url = SerializerMethodField()
    product = ProductSerializer(many=False)

    class Meta:
        model = Page
        fields = ('id', 'url', 'product')

    def get_url(self, instance):
        return instance.get_url()


class AuditLogSerializer(ModelSerializer):

    class Meta:
        model = AuditLog
        fields = ('id', 'page', 'price', 'created_at')
