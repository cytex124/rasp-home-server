from addons.price_control.models import Product, Page, AuditLog
from addons.price_control.tasks import collect_pricecontrol_data
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail


class CollectDataTest(TestCase):

    def setUp(self) -> None:
        # Create User
        self.user = User.objects.create(username='TestUser', email='test@test.com')
        # Create Test Product
        self.product = Product.objects.create(
            name='TestProduct',
            wish_price=999.00,
            currency='EUR',
            alarm_user=self.user
        )
        # Create Test page
        self.page = Page.objects.create(
            web_page='softairstore.de',
            suffix_url='/waffen/langwaffen/s-aeg-18/maschinenpistolen/kriss-vector/14099/kriss-vector-airsoft-in-schwarz-f-krytac',
            product=self.product
        )

    def test_collect_pricecontrol_data(self):
        collect_pricecontrol_data()
        self.assertEqual(len(AuditLog.objects.all()), 1, 'No AuditLog was created. Check it.')
        self.assertEqual(len(mail.outbox), 1, 'You should get a mail because wishprice is higher then currentprice. But you didn´t get an mail.')
