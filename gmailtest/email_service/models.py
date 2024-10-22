from django.db import models
from django_redis import get_redis_connection

class EmailMessage(models.Model):
    
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    receiver = models.EmailField()
    body = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    models.BinaryField()


    def __str__(self):
        return self.subject

