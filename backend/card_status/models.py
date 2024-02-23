from django.db import models

class CardStatus(models.Model):
    card_id = models.CharField(max_length=255, unique=True)
    user_mobile = models.CharField(max_length=255,)
    timestamp = models.DateTimeField(null=True)
    status = models.CharField(max_length=255)

    class Meta:
        db_table = "card_status"
        indexes = [
            models.Index(fields=['card_id', 'user_mobile',])
        ]
        ordering = ['timestamp']

    def __str__(self):
        return f"Card ID: {self.card_id}, User Mobile: {self.user_mobile}, Updated At: {self.timestamp}, Card Status: {self.status}"
