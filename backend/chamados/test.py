from rest_framework.test import APITestCase
from rest_framework import status
from .models import Chamado

class ChamadoFiltroTests(APITestCase):
    def setUp(self):
        # 1. Prepara o banco de dados de teste com 3 chamados diferentes
        Chamado.objects.create(titulo="Erro no sistema", descricao="...", status="ABERTO")
        Chamado.objects.create(titulo="Ajuste de tela", descricao="...", status="EM_ANDAMENTO")
        Chamado.objects.create(titulo="Atualização DB", descricao="...", status="CONCLUIDO")

    def test_filtro_por_status_valido(self):
        """A rota deve aceitar filtro por status e retornar somente os chamados correspondentes."""
        # Faz a requisição simulando o usuário: GET /api/chamados/?status=ABERTO
        response = self.client.get('/api/chamados/?status=ABERTO')
        
        # Verifica se deu sucesso (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se retornou apenas 1 chamado (o que criamos como ABERTO)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'ABERTO')

    def test_filtro_por_status_invalido(self):
        """Parâmetros inválidos devem ser tratados adequadamente com erro 400."""
        # Faz a requisição com um status que não existe
        response = self.client.get('/api/chamados/?status=BATATA')
        
        # Verifica se a API barrou a requisição com erro HTTP 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)