from django.db import models
from django.core.validators import MinValueValidator
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User


class RepoMaintainer(models.Model):
    repo_id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    alarm_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Repository Maintainer'
        verbose_name_plural = 'Repository Maintainers'
        ordering = ('repo_id',)

    def get_url(self):
        return 'https://apps.odoo.com/apps/browse?repo_maintainer_id={}'.format(self.repo_id)

    def get_product_links(self):
        response = requests.get(self.get_url())
        soup = BeautifulSoup(response.content, features="html.parser")
        product_cards = soup.find_all('div', 'loempia_app_entry')
        product_links = []
        for product_card in product_cards:
            link = 'https://apps.odoo.com{0}'.format(product_card.a['href'])
            product_links.append(link)
        return product_links

    def total_sales_price(self):
        total_sales = 0
        for product in OdooProduct.objects.filter(repo=self):
            total_sales += product.total_price()
        return total_sales

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.get_url())


class OdooProduct(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    url = models.CharField(max_length=256, null=False, blank=False)
    repo = models.ForeignKey(RepoMaintainer, related_name='odoo_product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Odoo Product'
        verbose_name_plural = 'Odoo Products'
        ordering = ('repo',)

    def total_price(self):
        total_price = 0
        for audit in AuditSalesCheck.objects.filter(product=self):
            total_price += audit.total_price()
        return total_price

    def total_amount(self):
        total = 0
        for audit in AuditSalesCheck.objects.filter(product=self):
            total += audit.amount
        return total

    def __str__(self):
        return '{0}'.format(self.name)


class AuditSalesCheck(models.Model):
    product = models.ForeignKey(OdooProduct, related_name='audit_sales_check', on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False)
    amount = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Audit Salescheck'
        verbose_name_plural = 'Audit Saleschecks'
        ordering = ('-created_at', 'product',)

    def total_price(self):
        return self.price * self.amount

    def __str__(self):
        return '{0}: {1}'.format(self.created_at, self.product)
