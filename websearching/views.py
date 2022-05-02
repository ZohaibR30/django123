from django.db.models.query import QuerySet
from rest_framework import viewsets
from .serializers import WebSearchingSerializer
from .models import websearching


# Create your views here.
class WebSearchingView(viewsets.ModelViewSet):
        serializer_class = WebSearchingSerializer
        queryset = websearching.objects.all()
    
