from django.core.management.base import BaseCommand
from addons.price_control.tasks import collect_pricecontrol_data


class Command(BaseCommand):
    help = 'Collect Pricecontrol Data'

    def handle(self, *args, **kwargs):
        collect_pricecontrol_data()
