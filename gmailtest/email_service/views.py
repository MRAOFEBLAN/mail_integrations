from django.shortcuts import render
from django.core.cache import cache
# Create your views here.

def index(request):
    return render(request, "index.html")



from rest_framework.views import APIView
from rest_framework.response import Response
from email_service.models import EmailMessage
from email_service.serializers import MessageSerializer

class MessageListView(APIView):
    def get(self, request):
        messages = EmailMessage.objects.all()
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)