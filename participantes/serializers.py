from rest_framework import serializers
from .models import Participantes

class ParticipantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participantes
        fields = '__all__'
