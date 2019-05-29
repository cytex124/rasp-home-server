from django.test import TestCase
from addons.price_control.models import Product, Page
from addons.price_control.serializers import PageSerializer
from django.contrib.auth.models import User
from addons.price_control.tasks import collect_pricecontrol_data
import json


class PageSerializerTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='TestUser', email='test@test.com')
        # Create Test Product
        self.product = Product.objects.create(
            name='TestProduct',
            wish_price=420.00,
            currency='EUR',
            alarm_user=self.user
        )
        # Create Test page
        self.page = Page.objects.create(
            web_page='softairstore.de',
            suffix_url='/waffen/langwaffen/s-aeg-18/maschinenpistolen/kriss-vector/14099/kriss-vector-airsoft-in-schwarz-f-krytac',
            product=self.product
        )
        # generate data
        collect_pricecontrol_data()
        collect_pricecontrol_data()

    def test_serializer(self):
        page_json = PageSerializer(instance=self.page).data
        self.assertIn('https://', page_json['url'])
        # Check Order of Auditlogs
        self.assertEqual(page_json['audit_logs'][0]['id'], 2)
        self.assertEqual(page_json['audit_logs'][1]['id'], 1)
        # Check Product
        self.assertEqual(page_json['product']['id'], 1)