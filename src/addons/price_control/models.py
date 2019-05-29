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

    def __str__(self):
        return self.name


class Page(models.Model):
    WEB_PAGES = (
        ('kotte-zeller.de', 'https://www.kotte-zeller.de'),
        ('softairstore.de', 'https://www.softairstore.de'),
        ('shoot-club.de', 'https://www.shoot-club.de'),
        ('softairwelt.de', 'https://www.softairwelt.de'),
        ('airsoft2go.de', 'https://airsoft2go.de')
    )
    web_page = models.CharField(max_length=64, choices=WEB_PAGES, null=False, blank=False)
    suffix_url = models.CharField(max_length=256, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Price Control Page'
        verbose_name_plural = 'Price Control Pages'

    def __str__(self):
        return '{0}{1}: {2}'.format(self.web_page, self.suffix_url, self.product)

    def get_url(self):
        return '{0}{1}'.format(dict(self.WEB_PAGES)[self.web_page], self.suffix_url)

    def get_current_price(self):
        response = requests.get(self.get_url())
        soup = BeautifulSoup(response.content, features="html.parser")
        return self._get_price(soup)

    def _get_price(self, soup):
        price = None
        locale.setlocale(locale.LC_ALL, 'de_DE')
        if self.web_page == 'kotte-zeller.de':
            price_text = soup.find_all('div', 'pr-price-normal')[0].find_all('span')[0].text
            price = locale.atof(price_text, decimal.Decimal)
        elif self.web_page == 'softairstore.de':
            price_text = soup.find_all('span', 'price--content')[0].find_all('meta')[0].get('content')
            price = decimal.Decimal(price_text)
        elif self.web_page == 'shoot-club.de':
            price_text = soup.find_all('div', 'prPrice')[0].text.split(' ')[0]
            price = locale.atof(price_text, decimal.Decimal)
        elif self.web_page == 'softairwelt.de':
            price_text = soup.find_all('span', 'price')[0].text.strip().split(' ')[0]
            price = locale.atof(price_text, decimal.Decimal)
        elif self.web_page == 'airsoft2go.de':
            price_text = soup.find_all('span', 'woocommerce-Price-amount')[0].text.strip().replace('€', '')
            price = locale.atof(price_text, decimal.Decimal)
        return price


class AuditLog(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Auditlog'
        verbose_name_plural = 'Auditlogs'

    def __str__(self):
        return '{}: {}'.format(self.page, self.price)
