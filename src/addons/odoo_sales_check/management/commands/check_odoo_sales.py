from django.core.management.base import BaseCommand
from addons.odoo_sales_check.tasks import check_odoo_sales


class Command(BaseCommand):
    help = 'Check Odoo Sales'

    def handle(self, *args, **kwargs):
        check_odoo_sales()
