from rest_framework import status
from rest_framework.test import APITestCase

from chamados.models import Chamado


class ChamadoTests(APITestCase):

    def test_nao_permite_cadastro_sem_titulo(self):
        dados = {
            "titulo": "",
            "descricao": "Chamado sem título",
            "status": "ABERTO",
        }

        resposta = self.client.post(
            "/api/chamados/",
            dados,
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", resposta.data)
        self.assertEqual(Chamado.objects.count(), 0)