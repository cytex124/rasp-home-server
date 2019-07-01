from django.core.management.base import BaseCommand
from addons.novarock_voting_bot.tasks import vote_on_novarock_page


class Command(BaseCommand):
    help = 'Vote on Noverock page'

    def handle(self, *args, **kwargs):
        vote_on_novarock_page()
