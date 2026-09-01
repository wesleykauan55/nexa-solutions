from rest_framework.test import APITestCase
from rest_framework import status
from .models import Chamado

class ChamadoFiltroTests(APITestCase):
    def setUp(self):
        # Criando massa de dados para o teste
        Chamado.objects.create(titulo="Erro no sistema", descricao="...", status="ABERTO")
        Chamado.objects.create(titulo="Ajuste de tela", descricao="...", status="EM_ANDAMENTO")
        Chamado.objects.create(titulo="Atualização DB", descricao="...", status="CONCLUIDO")

    def test_filtro_por_status_aberto_retorna_apenas_abertos(self):
        """A rota deve aceitar filtro por status e retornar somente os chamados correspondentes."""
        response = self.client.get('/api/chamados/?status=ABERTO')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'ABERTO')

    def test_filtro_por_status_invalido_retorna_erro_400(self):
        """Parâmetros inválidos devem ser tratados adequadamente (HTTP 400)."""
        response = self.client.get('/api/chamados/?status=INVALIDO')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criacao_chamado_sem_titulo_retorna_erro_400(self):
        """Não deve permitir a criação de um chamado com título vazio ou nulo."""
        payload = {
            "titulo": "",
            "descricao": "Problema no roteador",
            "status": "ABERTO"
        }
        response = self.client.post('/api/chamados/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('titulo', response.data)