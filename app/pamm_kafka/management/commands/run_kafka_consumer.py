from django.core.management.base import BaseCommand
from ...registry import list_registered_consumers
from ...consumer import MultiConsumer


class Command(BaseCommand):
    help = 'Fetch and apply Kafka messages'

    def handle(self, *args, **options):

        consumers = list_registered_consumers()
        for c in consumers:
            print('Found consumer: %s' % c)
        print('Running indefinite consumer...')
        multi = MultiConsumer(*consumers)
        multi.run()
