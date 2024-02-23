from rest_framework import serializers
from .models import CardStatus
from datetime import datetime

class CardStatusSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(source='timestamp', format='%Y-%m-%d %H:%M:%S')  # Use 'timestamp' field as 'updated_at' in the serializer

    class Meta:
        model = CardStatus
        fields = ['card_id', 'user_mobile', 'updated_at', 'status']
