from rest_framework import serializers
from .models import websearching

class WebSearchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = websearching
        fields = ('link','title','score', 'angle')