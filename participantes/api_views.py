from rest_framework import viewsets
from .models import Participantes
from .serializers import ParticipantesSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class ParticipantesViewSet(viewsets.ModelViewSet):
    queryset = Participantes.objects.all()
    serializer_class = ParticipantesSerializer


class BuscarParticipantePorCelularView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        celular = request.data.get('celular')

        if not celular:
            return Response(
                {"detail": "O número de celular é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            participante = Participantes.objects.get(celular=celular)
            serializer = ParticipantesSerializer(participante)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Participantes.DoesNotExist:
            return Response(
                {"detail": "Participante não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
