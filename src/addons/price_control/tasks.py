from __future__ import absolute_import, unicode_literals
from celery import task
from .models import Page, AuditLog, Product
from django.core.mail import EmailMessage


@task
def collect_pricecontrol_data():
    for page in Page.objects.all():
        price = page.get_current_price()
        audit_obj = AuditLog.objects.create(price=price, page=page)
        audit_obj.save()

    for product in Product.objects.all():
        lowest = None
        for page in Page.objects.filter(product=product):
            latest_audit = AuditLog.objects.filter(page=page).latest('created_at')
            if not lowest or latest_audit.price < lowest.price:
                lowest = latest_audit

        if lowest.price <= product.wish_price:
            email = EmailMessage(
                'Price Alarm: {}'.format(product.name),
                'See here: {}'.format(lowest.page.get_url()),
                to=[product.alarm_user.email]
            )
            email.send()
