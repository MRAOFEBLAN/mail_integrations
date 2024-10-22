from rest_framework import serializers
from email_service.models import EmailMessage

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmailMessage
        fields = '__all__'