# participantes/test_api.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from usuarios.models import Usuario # Supondo que seu modelo de usuário esteja em 'usuarios'
from .models import Participantes

class BuscarParticipanteAPITest(APITestCase):

    def setUp(self):
        """
        Configura o ambiente de teste antes de cada teste ser executado.
        """
        # 1. Cria um usuário de teste para autenticação
        self.user = Usuario.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        
        # 2. Autentica o cliente de teste com o token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # 3. Cria um participante de teste no banco de dados
        self.participante = Participantes.objects.create(
            nome='João da Silva Teste',
            cpf='11122233344',
            email='joao.teste@email.com',
            celular='5511999998888'
        )
        
        # 4. Define a URL do endpoint
        self.url = reverse('participantes:api_buscar_participante')

    def test_buscar_por_cpf_sucesso(self):
        """
        Verifica se a busca por um CPF existente retorna sucesso (200 OK) e os dados corretos.
        """
        payload = {'cpf': '111.222.333-44'}
        response = self.client.post(self.url, payload, format='json')

        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a resposta contém os dados esperados
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data'][0]['nome'], 'João da Silva Teste')

    def test_buscar_por_email_sucesso(self):
        """
        Verifica se a busca por um e-mail existente retorna sucesso.
        """
        payload = {'email': 'joao.teste@email.com'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_buscar_participante_nao_encontrado(self):
        """
        Verifica se a busca por um CPF inexistente retorna a mensagem de erro correta.
        """
        payload = {'cpf': '99988877766'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Participante não encontrado.')

    def test_requisicao_sem_identificador(self):
        """
        Verifica se a requisição sem nenhum identificador retorna erro.
        """
        payload = {} # Payload vazio
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['success'])
        self.assertIn('obrigatório', response.data['message'])