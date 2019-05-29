from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField, RelatedField
from .models import Product, Page, AuditLog


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        exclude = ('alarm_user', )


class AuditLogSerializer(ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id','price', 'created_at')


class PageSerializer(ModelSerializer):
    url = SerializerMethodField()
    product = ProductSerializer(many=False)
    audit_logs = SerializerMethodField()

    class Meta:
        model = Page
        fields = ('url', 'product', 'audit_logs')

    def get_url(self, instance):
        return instance.get_url()

    def get_audit_logs(self, instance):
        audit_logs = instance.audit_logs.all().order_by('-created_at')
        return AuditLogSerializer(audit_logs, many=True).data


