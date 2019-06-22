from .models import RepoMaintainer, OdooProduct, AuditSalesCheck
import requests
from bs4 import BeautifulSoup
import decimal
from django.core.mail import EmailMessage


def check_odoo_sales():
    for repo in RepoMaintainer.objects.all():
        product_links = repo.get_product_links()
        product_infos = get_product_infos_from_links(product_links)
        changes = []
        for product_info in product_infos:
            # Find or create new Product
            product = OdooProduct.objects.filter(url=product_info['url'])
            if not product:
                product = OdooProduct.objects.create(
                    repo=repo,
                    url=product_info['url'],
                    name=product_info['name']
                )
            else:
                product = product[0]
            audits = AuditSalesCheck.objects.filter(product=product)
            # If new Product --> no audits so create it
            if not audits:
                AuditSalesCheck.objects.create(
                    product=product,
                    price=product_info['price'],
                    amount=product_info['amount']
                )
            else:
                # If amount of sales changed create new audit
                product_total_amount = product.total_amount()
                if product_info['amount'] != product_total_amount:
                    new_amount = product_info['amount'] - product_total_amount
                    new_audit = AuditSalesCheck.objects.create(
                        product=product,
                        price=product_info['price'],
                        amount=new_amount
                    )
                    changes.append(new_audit)

        if repo.alarm_user and len(changes):
            send_mail_to_user(repo, changes)


def get_product_infos_from_links(product_links):
    product_infos = []
    for product_links in product_links:
        response = requests.get(product_links)
        soup = BeautifulSoup(response.content, features="html.parser")
        product_name = soup.find('h1', {'itemprop': 'name'}).text
        product_price = decimal.Decimal(soup.find('span', {'class': 'oe_currency_value'}).text)
        product_saled_amount = int(soup.find('span', {'title': 'Purchases'}).text)
        product_infos.append({
            'name': product_name,
            'price': product_price,
            'amount': product_saled_amount,
            'url': product_links
        })
    return product_infos


def send_mail_to_user(repo, changes):
    total = repo.total_sales_price()
    text = ''
    for change in changes:
        text += '- {0} {1}x{2} €'.format(change.product.name, change.amount, change.price)
    email = EmailMessage(
        'GG you saled something on ODOO!?!??!',
        body='New sale on: {0}.\r\nNew Total Sale: {1}\r\nNew Profit: {2.2f}'.format(
            text, total, total * 0.7
        ),
        to=[repo.alarm_user.email]
    )
    email.send()
