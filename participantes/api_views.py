from rest_framework import viewsets
from .models import Participantes
from .serializers import ParticipantesSerializer

class ParticipantesViewSet(viewsets.ModelViewSet):
    queryset = Participantes.objects.all()
    serializer_class = ParticipantesSerializer
