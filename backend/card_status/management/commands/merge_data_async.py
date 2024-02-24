from django.core.management.base import BaseCommand
from card_status import tasks

csv_files = {
    "pickup": "card_status/card-data/Sample Card Status Info - Pickup.csv",
    "delivery_exceptions": "card_status/card-data/Sample Card Status Info - Delivery exceptions.csv",
    "delivered": "card_status/card-data/Sample Card Status Info - Delivered.csv",
    "returned": "card_status/card-data/Sample Card Status Info - Returned.csv"
}

class Command(BaseCommand):
    help = 'Populate the database with data from CSV files using Celery Worker' 

    def handle(self, *args, **kwargs):
        tasks.pickup_csv_updated(csv_files['pickup']).delay()
        tasks.delivered_csv_updated(csv_files['delivered']).delay()
        tasks.delivery_exceptions_csv_updated(csv_files['delivery_exceptions']).delay()
        tasks.returned_csv_updated(csv_files['returned']).delay()
        
        self.stdout.write(self.style.SUCCESS('Data Merged Successfully'))
