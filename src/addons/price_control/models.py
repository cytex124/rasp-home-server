from django.db import models
import requests
from bs4 import BeautifulSoup
import locale
import decimal
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    img = models.ImageField(null=True, blank=True)
    wish_price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, null=False, blank=False, choices=(('EUR', '€'), ('DOL', '$')))
    alarm_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('alarm_user', 'name')

    def __str__(self):
        return self.name


class Page(models.Model):
    WEB_PAGES = (
        ('kotte-zeller.de', 'https://www.kotte-zeller.de', '_get_price_from_kotte_zeller_de'),
        ('softairstore.de', 'https://www.softairstore.de', '_get_price_from_softairstore_de'),
        ('shoot-club.de', 'https://www.shoot-club.de', '_get_price_from_shoot_club_de'),
        ('softairwelt.de', 'https://www.softairwelt.de', '_get_price_from_softairwelt_de'),
        ('airsoft2go.de', 'https://airsoft2go.de', '_get_price_from_airsoft2go_de')
    )
    web_page = models.CharField(max_length=64, choices=[(wp[0], wp[1]) for wp in WEB_PAGES], null=False, blank=False)
    suffix_url = models.CharField(max_length=256, null=False, blank=False)
    product = models.ForeignKey(Product, related_name='pages', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Price Control Page'
        verbose_name_plural = 'Price Control Pages'
        ordering = ('product', 'web_page')

    def __str__(self):
        return '{0}{1}: {2}'.format(self.web_page, self.suffix_url, self.product)

    def get_url(self):
        return '{0}{1}'.format(dict([(wp[0], wp[1]) for wp in self.WEB_PAGES])[self.web_page], self.suffix_url)

    def get_current_price(self):
        response = requests.get(self.get_url())
        soup = BeautifulSoup(response.content, features="html.parser")
        return self._get_price(soup)

    def _get_price(self, soup):
        price_text = None
        locale.setlocale(locale.LC_ALL, 'de_DE')
        for wp in self.WEB_PAGES:
            if wp[0] == self.web_page:
                price_text = eval('self.{}(soup)'.format(wp[2]))
                price_text = price_text.strip()

        if not price_text:
            raise NotImplementedError('{} func not found.'.format(self.web_page))
        elif price_text[-3] == ',' or ('.' in price_text and price_text[-3] != '.'):
            return locale.atof(price_text, decimal.Decimal)
        else:
            return decimal.Decimal(price_text)

    def _get_price_from_kotte_zeller_de(self, soup):
        return soup.find_all('div', 'pr-price-normal')[0].find_all('span')[0].text

    def _get_price_from_softairstore_de(self, soup):
        return soup.find_all('span', 'price--content')[0].find_all('meta')[0].get('content')

    def _get_price_from_shoot_club_de(self, soup):
        return soup.find_all('div', 'prPrice')[0].text.split(' ')[0]

    def _get_price_from_softairwelt_de(self, soup):
        return soup.find_all('span', 'price')[0].text.strip().split(' ')[0]

    def _get_price_from_airsoft2go_de(self, soup):
        return soup.find_all('span', 'woocommerce-Price-amount')[0].text.replace('€', '')


class AuditLog(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    page = models.ForeignKey(Page, related_name='audit_logs', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Auditlog'
        verbose_name_plural = 'Auditlogs'
        ordering = ('-created_at',)

    def __str__(self):
        return '{}: {}'.format(self.page, self.price)
