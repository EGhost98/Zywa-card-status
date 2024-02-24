from django.core.management.base import BaseCommand
from card_status import tasks

csv_files = {
    "pickup": "card_status/card-data/Sample Card Status Info - Pickup.csv",
    "delivery_exceptions": "card_status/card-data/Sample Card Status Info - Delivery exceptions.csv",
    "delivered": "card_status/card-data/Sample Card Status Info - Delivered.csv",
    "returned": "card_status/card-data/Sample Card Status Info - Returned.csv"
}

class Command(BaseCommand):
    help = 'Populate the database with data from CSV files'

    def handle(self, *args, **kwargs):
        tasks.returned_csv_updated(csv_files['returned'])
        tasks.delivered_csv_updated(csv_files['delivered'])
        tasks.delivery_exceptions_csv_updated(csv_files['delivery_exceptions'])
        tasks.pickup_csv_updated(csv_files['pickup'])
        
        self.stdout.write(self.style.SUCCESS('Data Merged Successfully'))
