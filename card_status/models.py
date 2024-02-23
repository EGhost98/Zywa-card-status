from django.db import models

class CardStatus(models.Model):
    card_id = models.CharField(max_length=255)
    user_mobile = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    card_status = models.CharField(max_length=255)
    
    class META:
        db_table = "card_status"
        indexes = [
            models.Index(fields=['card_id', 'user_mobile',])
        ]
        ordering = ['updated_at']

    def __str__(self):
        return f"Card ID: {self.card_id}, User Mobile: {self.user_mobile}, Updated At: {self.updated_at}, Card Status: {self.card_status}"
