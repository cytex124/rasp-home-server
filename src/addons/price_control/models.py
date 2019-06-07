from django.db import models
import requests
from bs4 import BeautifulSoup
import locale
import decimal
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


class Product(models.Model):
    """
    A Product object to notify a specific user.
    """
    name = models.CharField(max_length=256, null=False, blank=False)
    img = models.ImageField(null=True, blank=True)
    wish_price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, null=False, blank=False, choices=(('EUR', '€'), ('DOL', '$')))
    alarm_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('alarm_user', 'name')

    def send_mail(self, audit_log):
        """
        Send mail with price-alarm.
        :param audit_log: AuditLog-Model-Object
        :return: None
        """
        email = EmailMessage(
            'Price Alarm: {}'.format(self.name),
            'See here: {}'.format(audit_log.page.get_url()),
            to=[self.alarm_user.email]
        )
        email.send()

    def __str__(self):
        return self.name


class Page(models.Model):
    """
    Page Object is used to get price of product (X Pages for 1 Product) to compare prices on different pages.
    """
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
        """
        Get complete URL of Page-Object
        :return:
        url: string - example https://www.kotte-zeller.de/src-sr4-pe-light-sport-series-aeg-6mm-bb-schwarz
        """
        return '{0}{1}'.format(dict([(wp[0], wp[1]) for wp in self.WEB_PAGES])[self.web_page], self.suffix_url)

    def get_current_price(self):
        """
        Get Price of Product on Webpage
        :return:
        price: Decimal - example Decimal(400.00)
        """
        response = requests.get(self.get_url())
        soup = BeautifulSoup(response.content, features="html.parser")
        return self._get_price(soup)

    def _get_price(self, soup):
        """
        Get Price of bs4 soup object on webpage.
        :param
        soup: BS-Object - example BeautifulSoup(response.content, features="html.parser")
        :return:
        price: Decimal - example Decimal(400.00)
        """
        price_text = None
        locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
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
        try:
            return soup.find_all('div', 'pr-price-org')[0].find_all('span')[1].text
        except IndexError as _:
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
    """
    Auditlog of a Product on a Page. Just for logging reasons.
    """
    price = models.DecimalField(max_digits=8, decimal_places=2)
    page = models.ForeignKey(Page, related_name='audit_logs', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Auditlog'
        verbose_name_plural = 'Auditlogs'
        ordering = ('-created_at',)

    def __str__(self):
        return '{}: {}'.format(self.page, self.price)
