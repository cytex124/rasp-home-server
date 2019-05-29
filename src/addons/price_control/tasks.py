from __future__ import absolute_import, unicode_literals
from celery import task
from .models import PriceControlPage, AuditControl, ProductPriceControl
from django.core.mail import EmailMessage


@task
def collect_pricecontrol_data():
    for page in PriceControlPage.objects.all():
        price = page.get_current_price()
        audit_obj = AuditControl.objects.create(price=price, price_control_page=page)
        audit_obj.save()

    for product in ProductPriceControl.objects.all():
        lowest = None
        for page in PriceControlPage.objects.filter(product=product):
            latest_audit = AuditControl.objects.latest('created_at')
            if not lowest or latest_audit.price < lowest.price:
                lowest = latest_audit

        if lowest.price <= product.wish_price:
            email = EmailMessage('Price Alarm: {}'.format(product.name), 'See here: {}'.format(lowest.price_control_page.get_url()), to=[product.alarm_user.email])
            email.send()
