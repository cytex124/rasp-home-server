from addons.price_control.models import Product, Page
from django.test import TestCase
from django.contrib.auth.models import User
import decimal


class PageTest(TestCase):

    def setUp(self) -> None:
        # Create User
        self.user = User.objects.create(username='TestUser', email='test@test.com')
        # Create Test Product
        self.product = Product.objects.create(
            name='TestProduct',
            wish_price=420.00,
            currency='EUR',
            alarm_user=self.user
        )
        # Create Test pages (every page)
        self.pages = [
            {
                'url': 'https://www.kotte-zeller.de/kwa-kriss-vector-smg-gas-blow-back-6mm-bb-schwarz',
                'suffix': '/kwa-kriss-vector-smg-gas-blow-back-6mm-bb-schwarz',
                'web_page': 'kotte-zeller.de'
            },
            {
                'url': 'https://www.softairstore.de/waffen/langwaffen/s-aeg-18/maschinenpistolen/kriss-vector/14099/kriss-vector-airsoft-in-schwarz-f-krytac',
                'suffix': '/waffen/langwaffen/s-aeg-18/maschinenpistolen/kriss-vector/14099/kriss-vector-airsoft-in-schwarz-f-krytac',
                'web_page': 'softairstore.de'
            },
            {
                'url': 'https://www.shoot-club.de/Krytac-Kriss-Vector-SMG-AEG-05J-6mm-Airsoft-Maschinenpistole-ab14',
                'suffix': '/Krytac-Kriss-Vector-SMG-AEG-05J-6mm-Airsoft-Maschinenpistole-ab14',
                'web_page': 'shoot-club.de'
            },
            {
                'url': 'https://www.softairwelt.de/KRISS-Vector-Submachine-Gun-AEG-05-Joule-Softair-Bundle',
                'suffix': '/KRISS-Vector-Submachine-Gun-AEG-05-Joule-Softair-Bundle',
                'web_page': 'softairwelt.de'
            },
            {
                'url': 'https://airsoft2go.de/shop/airsoft/unter-05j-ab-14/krytac-kriss-vector-05-j',
                'suffix': '/shop/airsoft/unter-05j-ab-14/krytac-kriss-vector-05-j',
                'web_page': 'airsoft2go.de'
            }
        ]
        for index in range(len(self.pages)):
            self.pages[index]['page_object'] = Page.objects.create(
                web_page=self.pages[index]['web_page'],
                suffix_url=self.pages[index]['suffix'],
                product=self.product
            )

    def test_get_url(self):
        for page in self.pages:
            url = page['page_object'].get_url()
            self.assertEqual(url, page['url'])

    def test_get_current_price(self):
        for page in self.pages:
            price = page['page_object'].get_current_price()
            self.assertEqual(type(price), decimal.Decimal)
