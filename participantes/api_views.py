# gestor_campanha/participantes/api_views.py

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

class BuscarParticipanteView(APIView):
    """
    Endpoint unificado da API para buscar um participante por CPF, celular ou e-mail.
    A busca é feita na seguinte ordem de prioridade: CPF, depois e-mail, depois celular.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cpf = request.data.get('cpf')
        email = request.data.get('email')
        celular = request.data.get('celular')

        participante = None
        
        try:
            if cpf:
                # Limpa o CPF para uma busca robusta (remove pontos, traços, etc.)
                cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))
                participante = Participantes.objects.get(cpf=cpf_limpo)
            
            elif email:
                # Busca por e-mail ignorando maiúsculas/minúsculas
                participante = Participantes.objects.get(email__iexact=email)

            elif celular:
                # Busca por celular (pode ser melhorado com limpeza de caracteres)
                participante = Participantes.objects.get(celular=celular)
            
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Um dos campos (cpf, email ou celular) é obrigatório.",
                        "data": []
                    },
                    status=status.HTTP_200_OK
                )

            # Se encontrou o participante por qualquer um dos métodos
            serializer = ParticipantesSerializer(participante)
            return Response(
                {
                    "success": True,
                    "message": "Participante encontrado.",
                    "data": [serializer.data]
                },
                status=status.HTTP_200_OK
            )

        except Participantes.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Participante não encontrado.",
                    "data": []
                },
                status=status.HTTP_200_OK
            )