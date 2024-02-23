from celery import shared_task
import csv
from .models import CardStatus
from datetime import datetime
from django.utils import timezone
import re
from dateutil import parser
import pytz

@shared_task
def delivered_csv_updated(file):
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            card_id = row['Card ID']
            user_mobile = row['User contact']
            user_mobile = re.sub(r'\D', '', user_mobile)
            user_mobile = user_mobile[-9:]
            timestamp = parser.parse(row['Timestamp']).replace(tzinfo=pytz.utc)
            status = row['Comment']
            card_status = CardStatus.objects.filter(card_id=card_id, user_mobile=user_mobile).first()
            if card_status:
                if card_status.timestamp < timestamp:
                    card_status.status = status
                    card_status.timestamp = timestamp
                    card_status.save()
            else:
                CardStatus.objects.create(card_id=card_id, user_mobile=user_mobile, timestamp=timestamp, status=status)



@shared_task
def delivery_exceptions_csv_updated(file):
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            card_id = row['Card ID']
            user_mobile = row['User contact']
            user_mobile = re.sub(r'\D', '', user_mobile)
            user_mobile = user_mobile[-9:]
            timestamp = parser.parse(row['Timestamp']).replace(tzinfo=pytz.utc)
            status = row['Comment']
            card_status = CardStatus.objects.filter(card_id=card_id, user_mobile=user_mobile).first()
            if card_status:
                if card_status.timestamp < timestamp:
                    card_status.status = status
                    card_status.timestamp = timestamp
                    card_status.save()
            else:
                CardStatus.objects.create(card_id=card_id, user_mobile=user_mobile, timestamp=timestamp, status=status)




@shared_task
def pickup_csv_updated(file):
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            card_id = row['Card ID']
            user_mobile = row['User Mobile']
            user_mobile = re.sub(r'\D', '', user_mobile)
            user_mobile = user_mobile[-9:]
            timestamp = parser.parse(row['Timestamp']).replace(tzinfo=pytz.utc)
            status = "Picked Up"
            card_status = CardStatus.objects.filter(card_id=card_id, user_mobile=user_mobile).first()
            if card_status:
                if card_status.timestamp < timestamp:
                    card_status.status = status
                    card_status.timestamp = timestamp
                    card_status.save()
            else:
                CardStatus.objects.create(card_id=card_id, user_mobile=user_mobile, timestamp=timestamp, status=status)



@shared_task
def returned_csv_updated(file):
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            card_id = row['Card ID']
            user_mobile = row['User contact']
            user_mobile = re.sub(r'\D', '', user_mobile)
            user_mobile = user_mobile[-9:]
            timestamp = parser.parse(row['Timestamp']).replace(tzinfo=pytz.utc)
            status = "Returned"
            card_status = CardStatus.objects.filter(card_id=card_id, user_mobile=user_mobile).first()
            if card_status:
                if card_status.timestamp < timestamp:
                    card_status.status = status
                    card_status.timestamp = timestamp
                    card_status.save()
            else:
                CardStatus.objects.create(card_id=card_id, user_mobile=user_mobile, timestamp=timestamp, status=status)

